import contextlib
import logging

from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.middleware.cors import CORSMiddleware

from api.constants import ApiSpecTags
from api.router import health_check, v1_router

logging.basicConfig()
logger = logging.getLogger(__name__)


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("See the Swagger docs at http://localhost:9000/docs")
    yield


app = FastAPI(title="GSW AIT API", lifespan=lifespan)


app.get(
    "/healthz",
    tags=[ApiSpecTags.OTHER],
)(health_check)
app.include_router(v1_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def use_route_names_as_operation_ids(app: FastAPI) -> None:
    """
    https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/#using-the-path-operation-function-name-as-the-operationid
    Simplify operation IDs so that generated API clients have simpler function
    names.

    Should be called only after all routes have been added.
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name


use_route_names_as_operation_ids(app)
