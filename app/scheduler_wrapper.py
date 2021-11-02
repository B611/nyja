#!/usr/bin/python3.8
import sys
import requests
import os


def send_job(args):
    if len(args):
        params = {"command": args[0], "address": args[1]
                  if len(args) == 2 else "", "save": True}
        requests.post(
            os.environ["REACT_APP_NYJA_API"] + "/run_task", json=params)


if __name__ == '__main__':
    send_job(sys.argv[1:])
