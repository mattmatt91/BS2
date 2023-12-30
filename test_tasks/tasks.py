from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
import asyncio

class Tasks():
    def __init__(self) -> None:
        print("init task instance")
        self.scheduler = AsyncIOScheduler()


    async def start_scheduler(self):
        # Schedule tasks
        self.scheduler.add_job(
            self.measure_data,
            trigger=IntervalTrigger(seconds=10)
        )

        self.scheduler.add_job(
            self.toggle_lamp_on,
            trigger=CronTrigger(second=0),
            id="lamp_on"
        )
        self.scheduler.add_job(
            self.toggle_lamp_off,
            trigger=CronTrigger(second=30),
            id="lamp_off"
        )
        self.scheduler.start()
     
    async def toggle_lamp_off(self):
        print("lamp off")

    async def toggle_lamp_on(self):
        print("lamp on")

    async def measure_data(self):
        print("measure data")

async def main():
    task = Tasks()
    # Run the scheduler in the background
    await asyncio.sleep(10)  # or any other duration or logic to keep the script running

if __name__ == "__main__":
    asyncio.run(main())
