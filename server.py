#!/usr/bin/env python3

from bottle import post, run, request
import urllib3
import json

http = urllib3.PoolManager()


@post("/hook")
def hook():
    req = request.json
    tag = req["push_data"]["tag"]
    branch = "stable" if tag == "latest" else "dev"
    callback = req["callback_url"]
    target_prefix = "dev." if tag == "dev" else ""
    r = http.request("POST", callable, json.dumps({
        "state": "success",
        "description": "",
        "context": f"Deploy {branch} branch",
        "target_url": f"https://{target_prefix}yituliu.site"
    }).encode("utf-8"))
    return (f"callback: {callback}, branch: {branch}")


run(host="0.0.0.0", port=11000)
