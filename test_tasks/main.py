from fastapi import FastAPI
try:
    from test_tasks.tasks import Tasks
except:
    from tasks import Tasks
    
app = FastAPI()

@app.on_event("startup")
@app.get("/startup")
async def start_tasks():
    print("startup ...")
    tasks = Tasks()
    print(tasks)

    await tasks.start_scheduler()

