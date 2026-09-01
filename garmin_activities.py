import os
import sys

from dotenv import load_dotenv
from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
)

load_dotenv()

email = os.getenv("GARMIN_EMAIL")
password = os.getenv("GARMIN_PASSWORD")
tokenstore = os.getenv("GARMIN_TOKENSTORE", os.path.expanduser("~/.garminconnect"))

try:
    client = Garmin(email=email, password=password)
    client.login(tokenstore)
except (GarminConnectAuthenticationError, GarminConnectConnectionError) as err:
    sys.exit(f"No se pudo conectar con Garmin: {err}")

activities = client.get_activities(0, 5)
assert isinstance(activities, list)

for activity in activities:
    print(f"{activity['startTimeLocal']} - {activity['activityName']}")
