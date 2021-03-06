import http

import requests as req
from flask import Flask, request

from LB import LB


class AppError(Exception):
    def __init__(self, msg, code):
        super().__init__(msg)
        self.message = msg
        self.code = code


class NoInstancesAvailable(AppError):
    def __init__(self):
        super().__init__("There are no server instances currently available", http.HTTPStatus.SERVICE_UNAVAILABLE)


app = Flask(__name__)
load_balancer = LB()


@app.errorhandler(AppError)
def error_handler(e):
    return e.message, e.code


@app.route("/", defaults={'path': ''})
@app.route('/<path:path>')
def all_routes(path):
    if load_balancer.reachable_container_amount == 0:
        raise NoInstancesAvailable()

    url = "http://" + load_balancer.next() + path

    response = req.request(
        method=request.method,
        url=url,
        params=request.args,
        data=request.data
    )

    return (response.text, response.status_code, response.headers.items())


if __name__ == '__main__':
    app.run(port=8090, threaded=True)
