#!/usr/bin/env python3

from ngeprint import app, socket_io

if __name__ == "__main__":
	socket_io.run(app, port=8000, debug=True)
