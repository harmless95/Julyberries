import uvicorn
from fastapi import FastAPI

from api.v1 import router_v1
from core.config import setting

app_main = FastAPI()
app_main.include_router(router=router_v1)


@app_main.get("/")
async def get_hello():
    return {"message": "Hello, this is the authorization container."}


if __name__ == "__main__":
    uvicorn.run(
        "main:app_main",
        host=setting.run.host,
        port=setting.run.port,
    )
