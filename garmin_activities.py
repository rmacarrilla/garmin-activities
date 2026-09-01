from garmin_client import get_client

client = get_client()

activities = client.get_activities(0, 5)
assert isinstance(activities, list)

for activity in activities:
    print(f"{activity['startTimeLocal']} - {activity['activityName']}")
