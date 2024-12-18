from fastapi import FastAPI
import uvicorn
from app.router import router
import logging

app = FastAPI()

app.include_router(router)


if __name__ == "__main__":
   logging.basicConfig(level=logging.INFO)

   uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
