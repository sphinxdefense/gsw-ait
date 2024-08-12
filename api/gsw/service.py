from datetime import datetime as dt
import logging


from api.settings import Settings

logger = logging.getLogger(__name__)
settings = Settings()


def get_packets(client, model):
    start_time = dt.strptime(model.start_time, "%Y-%m-%dT%H:%M:%S")
    end_time = dt.strptime(model.end_time, "%Y-%m-%dT%H:%M:%S")
    AITDBResult = client.query_packets(
        packets=[model.packet], start_time=start_time, end_time=end_time
    )
    result = []
    packets = AITDBResult.get_packets()
    for packet in packets:
        logger.info(packet.toJSON())
        result.append(packet.toJSON())
    logger.info(result)
    return {"packets": result}
