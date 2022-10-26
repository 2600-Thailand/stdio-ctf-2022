
import json

x = []
for i in range(1024):
    x.append({
        "deal": f"FREE{i} EVERYTHING",
        "code": f"FREE{i}",
        "value": 0,
        "detail": "One coupon per person",
        "expired": "Valid till 31 Dec 2022",
        "status": False
    })

print(json.dumps(x))