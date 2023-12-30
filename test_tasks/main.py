from fastapi import FastAPI
try:
    from test_tasks.tasks import Tasks
except:
    from tasks import Tasks
    
app = FastAPI()

@app.on_event("startup")
async def start_tasks():
    tasks = Tasks()
    await tasks.start_scheduler()
    print("startup ...")
