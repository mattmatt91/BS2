import asyncio
import RPi.GPIO as GPIO
import time
from concurrent.futures import ThreadPoolExecutor


class WaterLevelSensor:
    def __init__(self, GPIO_TRIGGER: int, GPIO_ECHO: int):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(GPIO_ECHO, GPIO.IN)
        self.GPIO_TRIGGER = GPIO_TRIGGER
        self.GPIO_ECHO = GPIO_ECHO

    def get_distance_sync(self):
        GPIO.output(self.GPIO_TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(self.GPIO_TRIGGER, False)

        StartZeit = time.time()
        StopZeit = time.time()

        while GPIO.input(self.GPIO_ECHO) == 0:
            StartZeit = time.time()

        while GPIO.input(self.GPIO_ECHO) == 1:
            StopZeit = time.time()

        TimeElapsed = StopZeit - StartZeit
        distance = (TimeElapsed * 34300) / 2

        return distance

    async def get_distance(self):
        loop = asyncio.get_running_loop()
        with ThreadPoolExecutor() as pool:
            distance = await loop.run_in_executor(pool, self.get_distance_sync)
            return distance


if __name__ == "__main__":
    # Example usage
    async def main():
        sensor = WaterLevelSensor(GPIO_TRIGGER=17, GPIO_ECHO=27)
        try:
            while True:
                distance = await sensor.get_distance()
                print(f"Distance: {distance} cm")
                await asyncio.sleep(1)  # Asynchronous delay
        except KeyboardInterrupt:
            GPIO.cleanup()

    asyncio.run(main())
