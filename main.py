import logging

from fastapi import FastAPI
from fastapi_utils.timing import add_timing_middleware
from starlette.middleware.cors import CORSMiddleware

from routes import ontomatch

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=f"Ontology Matching API",
    description="Ontology Matching API.",
    version="0.1",
    docs_url="/docs",
    openapi_url=f"/v1/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

add_timing_middleware(app, record=logger.info, prefix="app", exclude="untimed")

app.include_router(ontomap.router)

