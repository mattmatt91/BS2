from fastapi import FastAPI
try:
    from test_tasks.tasks import Tasks
except:
    from tasks import Tasks
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
tasks = Tasks()

# Middleware (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
# @app.get("/startup")
async def start_tasks():
    print("startup ...")
    print(tasks)
    await tasks.start_scheduler()

@app.get("/startup")
async def test_route():
    return "test"
