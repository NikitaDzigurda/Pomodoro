from fastapi import FastAPI
from handlers import routers


app = FastAPI(redoc_url=None)
for router in routers:
    app.include_router(router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
