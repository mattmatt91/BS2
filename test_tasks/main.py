from fastapi import FastAPI
from tasks import Tasks

app = FastAPI()

@app.on_event("startup")
async def start_tasks():
    tasks = Tasks()
    await tasks.start_scheduler()
    print("startup ...")

# Additional FastAPI routes and logic go here
