from flask import Flask
from json import load

config = None
try:
	with open("config.json") as f:
		config = load(f)
	f.close()
except FileNotFoundError as error:
	print(error)
finally:
	if not config:
		exit()

app = Flask(__name__)

import ngeprint.customer_routes
import ngeprint.admin_routes
import ngeprint.api_routes
