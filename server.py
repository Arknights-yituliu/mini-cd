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
        name = "v2plus-stable"
        port = 10001
        target_prefix = ""
    else:  # tag = "dev"
        branch = "dev"
        name = "v2plus"
        port = 10000
        target_prefix = "dev."
    callback = req["callback_url"]
    http.request("POST", callback,  body=json.dumps({
        "state": "success",
        "description": "",
        "context": f"Deploy {branch} branch",
        "target_url": f"https://{target_prefix}yituliu.site"
    }).encode("utf-8"), headers={'Content-Type': 'application/json'})
    Popen(
        f"docker pull zhaozuohong/yituliu-frontend-v2-plus:{tag} && docker stop {name} && docker run -d --rm --name {name} -e PORT={port} -p {port}:{port} zhaozuohong/yituliu-frontend-v2-plus:{tag}", shell=True)
    return (f"callback: {callback}, branch: {branch}")


run(host="0.0.0.0", port=11000)
