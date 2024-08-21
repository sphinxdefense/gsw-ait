from datetime import datetime
import logging
from faker import Faker
from faker.providers import geo

fake = Faker()
fake.add_provider(geo)


from api.settings import Settings

logger = logging.getLogger(__name__)
settings = Settings()


def get_packets(client, model):
    start_time = datetime.strptime(model.start_time, "%Y-%m-%dT%H:%M:%S")
    end_time = datetime.strptime(model.end_time, "%Y-%m-%dT%H:%M:%S")
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


def get_contact(model):
    lat, long = fake.latlng()
    return {
        "aos": 1724011334001,  # int(time.time()), #datetime.now(timezone.utc).isoformat(),
        "los": 1724012606001,  # int(time.time()) + 60*10, #(datetime.now(timezone.utc) + timedelta(minutes=10)).isoformat(),
        "id": model.contact_id,
        "iron": 9999,
        "norad_id": 99999,
        "name": 6619323894333440,
        "type": "contact",
        "priority": "low",
        "status": "normal",
        "ground": "AWS",
        "rev": 3856,
        "satellite": "nos3",
        "state": "executing",
        "step": "Lock",
        "detail": "nos3 Simulation",
        "dayOfYear": 231,
        "latitude": float(lat),
        "longitude": float(long),
        "azimuth": float(long),
        "elevation": 30.0,
        "mode": "automatic",
        "resolution": "pass",
        "resolutionStatus": "normal",
        "selected": True,
    }
