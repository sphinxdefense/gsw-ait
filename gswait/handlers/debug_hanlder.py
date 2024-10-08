import ait.core.log
import time
from ait.core.server.handler import Handler

# import pickle  # nosec


class DebugHandler(Handler):
    def __init__(self, input_type=None, output_type=None, **kwargs):
        super(DebugHandler, self).__init__(input_type, output_type)
        self.data = []
        self.time = time.time()
        self.file_write_done = False

    def handle(self, input_data):
        new_time = time.time()
        ait.core.log.info(f"Packet rx delta: {new_time - self.time}")
        self.time = new_time
        ait.core.log.info(
            f"Debug handler received {len(input_data)} bytes: {input_data}"
        )
        # ait.core.log.info(input_data)
        # self.data.append(input_data)
        # if len(self.data) > 1000 and not self.file_write_done:
        #     self.file_write_done = True
        #     fname = "/tmp/nos3/packets.pkl"  # nosec
        #     ait.core.log.info(f"Writing data to file: {fname}")
        #     with open(fname, "wb") as f:
        #         pickle.dump(self.data, f)
        return input_data
