#!/usr/bin/env python3

from datetime import datetime, timedelta
from ngeprint import dao, job_dao
from os import remove
from os.path import exists
from shutil import rmtree
from time import sleep

def loop():
    temp = False
    if exists("loop"):
        with open("loop") as f:
            temp = int(f.read()) > 0
        f.close()
    return temp

def handle_unconfirmed(job):
    date = datetime.strptime(job["tanggal"], "%Y-%m-%d %H:%M:%S.%f")
    delta = datetime.now() - date
    if delta.seconds > 10800: # 3 hours
        print("delete id: {}".format(job["id"]))
        remove(job["server_file"])
        rmtree("{}/{}".format("temp", job["id"]))
        success, num_rows, error = job_dao.delete(job["id"])
        if not success:
            print(str(error))

def handle_confirmed(job):
    print("id: {}".format(job["id"]))

while loop():
    success, jobs, error = job_dao.retrieve()
    if not success:
        print(str(error))
    for job in jobs:
        eval("handle_{}(job)".format(job["status"].lower()))
    sleep(1)
