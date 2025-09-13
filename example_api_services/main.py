import uvicorn
from fastapi import FastAPI
from api.example_API_router import router
from core.config import setting

app = FastAPI()
app.include_router(router=router)

if __name__ == "__main__":
    uvicorn.run("main:app", host=setting.run.host, port=setting.run.port)
