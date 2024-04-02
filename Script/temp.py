from datetime import datetime, timedelta

today = datetime.today()
start = datetime.today() - timedelta(days=100)
print(start, today)

