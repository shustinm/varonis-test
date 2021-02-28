from sanic import Sanic
from sanic.request import Request
from sanic_jwt import initialize, protected
from auth import authenticate

app = Sanic(name='Normalizer')
initialize(app, authenticate=authenticate)


@app.post('/normalize')
@protected
def normalize(request: Request):
    pass


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8888)