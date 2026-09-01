import os
import sys

from dotenv import load_dotenv
from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
)


def get_client() -> Garmin:
    load_dotenv()

    email = os.getenv("GARMIN_EMAIL")
    password = os.getenv("GARMIN_PASSWORD")
    tokenstore = os.getenv("GARMIN_TOKENSTORE", os.path.expanduser("~/.garminconnect"))

    try:
        client = Garmin(email=email, password=password)
        client.login(tokenstore)
    except (GarminConnectAuthenticationError, GarminConnectConnectionError) as err:
        sys.exit(f"No se pudo conectar con Garmin: {err}")

    return client
