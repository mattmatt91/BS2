from fastapi import FastAPI
try:
    from test_tasks.tasks import Tasks
except:
    from tasks import Tasks
    
app = FastAPI()
tasks = Tasks()

@app.on_event("startup")
# @app.get("/startup")
async def start_tasks():
    print("startup ...")
    print(tasks)
    await tasks.start_scheduler()

