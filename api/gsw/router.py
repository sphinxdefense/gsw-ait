import logging

from fastapi import APIRouter, Depends
from api.gsw import schemas, service
from api.dependencies import InfluxClient

logger = logging.getLogger(__name__)
router = APIRouter()


# Targets
#########################################################################
@router.get("/packets", response_model=schemas.PacketResponse)
def get_packets(client: InfluxClient, model: schemas.PacketQuery = Depends()):
    return service.get_packets(client, model)


@router.get("/contact", response_model=schemas.ContactResponse)
def get_contact(model: schemas.ContactQuery = Depends()):
    return service.get_contact(model)
