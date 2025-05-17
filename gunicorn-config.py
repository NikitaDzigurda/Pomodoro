import os
from uvicorn.workers import UvicornWorker
from dotenv import load_dotenv

bind = '0.0.0.0:8000'
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"

environment = os.getenv("ENVIRONMENT")

env = os.path.join(os.getcwd(), f".{environment}.env")
if os.path.exists(env):
    load_dotenv(env)
