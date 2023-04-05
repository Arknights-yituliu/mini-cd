#!/usr/bin/env python3

from bottle import post, run, request
import urllib3
import json
from subprocess import Popen

http = urllib3.PoolManager()


@post("/hook")
def hook():
    req = request.json
    tag = req["push_data"]["tag"]
    callback = req["callback_url"]
    http.request("POST", callback,  body=json.dumps({
        "state": "success",
        "description": "",
        "context": "",
        "target_url": ""
    }).encode("utf-8"), headers={'Content-Type': 'application/json'})
    if tag == "dev":
        Popen(
            "docker pull zhaozuohong/yituliu-frontend-v2-plus:dev && docker stop v2plus && docker run -d --rm --name v2plus -e PORT=10000 -p 10000:10000 zhaozuohong/yituliu-frontend-v2-plus:dev", shell=True)

    return ("OK")


run(host="0.0.0.0", port=11000)
