import pickle  # nosec
import ait.core.log

from ait.core.server.handler import Handler
from gswait.settings import CCSDS_PRIMARY_HEADER_LEN
from ait.core import tlm


class CCSDSPacketHandler(Handler):
    """
    This CCSDS handler provides a way to accept multiple packet types on a
    single stream and have them be processed. This handler takes a string of
    raw binary data containing CCSDS packet data. It maps the APID of
    the packet to a packet name from the config, and then uses the packet name
    to get the UID from the default telemetry dictionary. The user data field
    is extracted from the raw binary data, and a tuple of the UID and user data
    field is returned.
    """

    def __init__(self, input_type=None, output_type=None, **kwargs):
        """
        Params:
            input_type:   (optional) Specifies expected input type, used to
                                     validate handler workflow. Defaults to None.
            output_type:  (optional) Specifies expected output type, used to
                                     validate handler workflow. Defaults to None
            packet_types: (required) APID value (string) : packet name (string) pairs
                                     APID value can use 'X' to mask out a bit
                                     For example, 'XXXXX1011XXX' means only bits 6-9 represent the APID
            packet_secondary_header_length: (optional) Length of secondary header in octets.
                                                       Defaults to 0.
        Raises:
            ValueError:   If packet in config is not present in default tlm dict.
        """
        super(CCSDSPacketHandler, self).__init__(input_type, output_type)
        self.hdr_name = kwargs.get("hdr_name", "CCSDS_HEADER")
        self.tlm_dict = ait.core.tlm.getDefaultDict()
        self.hdr_def = self.tlm_dict[self.hdr_name]
        self.packet_types = kwargs.get("packet_types", {})
        self.packet_secondary_header_length = kwargs.get(
            "packet_secondary_header_length", 0
        )

        # Check if all packet names in config are in telemetry dictionary
        for packet_name in self.packet_types.values():
            if packet_name not in self.tlm_dict.keys():
                msg = "CCSDSPacketHandler: Packet name {} not present in telemetry dictionary.".format(
                    packet_name
                )
                msg += " Available packet types are {}".format(self.tlm_dict.keys())
                raise ValueError(msg)

    def handle(self, input_data):
        """
        Params:
            packet:    CCSDS packet
        Returns:
            tuple of packet UID and packet data field
        """
        if (
            len(input_data)
            < CCSDS_PRIMARY_HEADER_LEN + self.packet_secondary_header_length + 1
        ):
            ait.core.log.info(
                f"CCSDSPacketHandler: Received packet length is less than minimum of {CCSDS_PRIMARY_HEADER_LEN+self.packet_secondary_header_length+1} bytes."
            )
            return
        ait.core.log.debug(
            f"CCSDSPacketHandler: Received packet length of {len(input_data)}"
        )
        ccsds_hdr = tlm.Packet(
            self.hdr_def,
            data=input_data[
                0 : CCSDS_PRIMARY_HEADER_LEN + self.packet_secondary_header_length
            ],
        )
        stream_id = int(ccsds_hdr.stream_id)

        if stream_id not in self.packet_types:
            msg = f"CCSDSPacketHandler: Packet APID {stream_id} not present in config - Available packet APIDs are {self.packet_types.keys()}"
            ait.core.log.info(msg)
            return
        # Map APID to packet name in config to get UID from telemetry dictionary
        packet_name = self.packet_types[stream_id]
        packet_uid = self.tlm_dict[packet_name].uid
        # ait.core.log.info(
        #     f"CCSDSPacketHandler - handling packet: {packet_name} - id: {packet_uid}"
        # )
        # Extract user data field from packet
        packet_data_length = ccsds_hdr.packet_length
        # ait.core.log.info(f"{packet_data_length} - {len(input_data)}")
        if len(input_data) < CCSDS_PRIMARY_HEADER_LEN + packet_data_length:
            ait.core.log.info(
                "CCSDSPacketHandler: Packet data length is less than stated length in packet primary header."
            )
            return
        udf_length = packet_data_length - self.packet_secondary_header_length
        udf_start = CCSDS_PRIMARY_HEADER_LEN + self.packet_secondary_header_length
        user_data_field = input_data[udf_start : udf_start + udf_length + 1]
        ait.core.log.debug(
            f"CCSDSPacketHandler: Handling APID {stream_id} with length: {len(user_data_field)}"
        )
        return pickle.dumps((packet_uid, user_data_field), 2)

    def comp_apid(self, server_apid):
        """
        Params:
            server_apid:  APID from server
        Returns:
            Matching config_apid if one is present in config
            None otherwise
        """
        for config_apid in self.packet_types:
            match = True
            for i in range(11):
                if config_apid[i] != "X" and config_apid[i] != server_apid[i]:
                    match = False
                    break
            if match:
                return config_apid
        return None
