import requests
import time
import json
import logging
from quixstreams import Application
import random


def get_weather():
    response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": int(random.randrange(-90,90)),
            "longitude": int(random.randrange(-180,180)),
            "current": "temperature_2m",
        },
    )

    return response.json()


def main():
    app = Application(
        broker_address="localhost:9095",
        loglevel="DEBUG",
    )

    with app.get_producer() as producer:
        while True:
            weather = get_weather()
            logging.debug("Got weather: %s", weather)
            producer.produce(
                topic="weather_data",
                key="Random",
                value=json.dumps(weather),
            )
            logging.info("Produced. Sleeping...")
            time.sleep(10)


if __name__ == "__main__":
    logging.basicConfig(level="DEBUG")
    main()