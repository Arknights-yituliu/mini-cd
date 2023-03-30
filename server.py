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
    if tag == "latest":
        branch = "stable"
        target_prefix = ""
    else:  # tag = "dev"
        branch = "dev"
        target_prefix = "dev."
    callback = req["callback_url"]
    http.request("POST", callback,  body=json.dumps({
        "state": "success",
        "description": "",
        "context": f"Deploy {branch} branch",
        "target_url": f"https://{target_prefix}yituliu.site"
    }).encode("utf-8"), headers={'Content-Type': 'application/json'})
    if tag == "latest":
        Popen(
            "docker pull zhaozuohong/yituliu-frontend-v2-plus:latest", shell=True)
    else:
        Popen(
            "docker pull zhaozuohong/yituliu-frontend-v2-plus:dev && docker stop v2plus && docker run -d --rm --name v2plus -e PORT=10000 -p 10000:10000 zhaozuohong/yituliu-frontend-v2-plus:dev", shell=True)

    return (f"callback: {callback}, branch: {branch}")


run(host="0.0.0.0", port=11000)
