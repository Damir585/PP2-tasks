from datetime import datetime, timedelta


now = datetime.now()
print("Current date and time:", now)


yesterday = now - timedelta(days=1)
print("Yesterday:", yesterday)


tomorrow = now + timedelta(days=1)
print("Tomorrow:", tomorrow)