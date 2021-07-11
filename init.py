from cryptography.fernet import Fernet
from ngeprint import config_dao
from json import dumps

user = {"username": "admin", "password": "nimda"}

key = Fernet.generate_key()
fern = Fernet(key)
user["password"] = fern.encrypt(user["password"].encode("utf-8")).decode("utf-8")

configs = [
    {"_key": "user.username", "_value": user["username"]},
    {"_key": "user.password", "_value": user["password"]},
    {"_key": "price.grayscale", "_value": 1000},
    {"_key": "price.color", "_value": 1500},
    {"_key": "price.blank", "_value": 500}
]

for conf in configs:
    config_dao.create(conf)

with open("key.txt", "w") as f:
    f.write(key.decode("utf-8"))
f.close()
