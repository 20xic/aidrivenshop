import uvicorn

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from contextlib import asynccontextmanager
from core import settings,logger
from core.model import db_helper
from api import router as api_router


@asynccontextmanager
async def lifespan(FastAPI):
    logger.info("Application is starting")
    yield
    logger.info("Application is shuting down")
    await db_helper.dispose() 
   

app = FastAPI(lifespan=lifespan,default_response_class=ORJSONResponse)
app.include_router(api_router)

if __name__=="__main__":
    uvicorn.run(
        "main:app",host=settings.run.host,port=settings.run.port,reload=True
    )