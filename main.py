from sanic import Sanic
from sanic.request import Request
from sanic.response import json
from sanic_jwt import initialize, protected
from auth import authenticate
import re


def create_app():

    app = Sanic(name='Normalizer')
    initialize(app, authenticate=authenticate)

    # Regex to search for "val", case insensitive
    r = re.compile(r'.*val.*', flags=re.IGNORECASE)

    @app.post('/normalize')
    @protected()
    def normalize(request: Request):
        return json(
            {d['name']: d[next(filter(r.match, d))] for d in request.json}
        )

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=8888)