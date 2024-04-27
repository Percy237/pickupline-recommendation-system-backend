import os
import django
import json
from datetime import datetime

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

# Configure Django's settings
django.setup()

# Load existing user fixtures from a JSON file
with open("existing_users.json", "r") as f:
    existing_users = json.load(f)


def generate_user_fixture(username_prefix, count):
    users = []
    for i in range(1, count + 1):
        username = f"{username_prefix}{i}"
        user = {
            "model": "auth.user",
            "pk": i,
            "fields": {
                "password": "pbkdf2_sha256$720000$XhNF3ckgFdrUaZpumZNw8S$thXMxRC8rFjFFLrPN35Tk4rdtGe063q/Pv75kdFgdy8=",
                "last_login": None,
                "is_superuser": False,
                "username": username,
                "first_name": "",
                "last_name": "",
                "email": f"{username}@example.com",
                "is_staff": False,
                "is_active": True,
                "date_joined": datetime.now().isoformat(),
                "groups": [],
                "user_permissions": [],
            },
        }
        users.append(user)
    return users


# Generate 100 additional users with username prefix "user"
additional_users = generate_user_fixture("user", 100)

# Append the additional users to the existing_users.json file
with open("existing_users.json", "a") as f:
    for user in additional_users:
        f.write(json.dumps(user) + "\n")
