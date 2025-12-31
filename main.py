from app import create_app
from flask_cors import CORS
from flask import request, abort, Response, session
from flask.json.provider import JSONProvider
from datetime import date, datetime
import json


from flask.json.provider import JSONProvider
import json
from datetime import date, datetime
import werkzeug.wrappers

"""
class ImprovedJsonProvider(JSONProvider):
    def __init__(self, *args, **kwargs):
        self.options = kwargs
        super().__init__(*args, **kwargs)
    
    def default(self, o):
        print('default')
        if isinstance(o, datetime):
            return o.strftime("%m/%d/%Y, %H:%M:%S")
        elif isinstance(o, date):
            return o.strftime("%m/%d/%Y")
        return super().default(o)

    def dumps(self, obj, **kwargs):
        print('dumps')
        kwargs.setdefault("default", self.default)
        kwargs.setdefault("ensure_ascii", True)
        kwargs.setdefault("sort_keys", True)
        return json.dumps(obj, **kwargs)

    def loads(self, s: str | bytes, **kwargs):
        print('loads')
        if isinstance(s, bytes):
            s = s.decode('utf-8')

        s_dict: dict = json.loads(s)
        s_sanitized = {k: v for k, v in s_dict.items() if v}
        s_str = json.dumps(s_sanitized)
        return json.loads(s_str, **kwargs)


class AppMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = werkzeug.wrappers.Request(environ)
        api_path = request.url
        print(f'accessing URL endpoint: {api_path} ')
        iterator:werkzeug.wsgi.ClosingIterator = self.app(environ, start_response)
        response = werkzeug.wrappers.Response(start_response)
        print(f'exiting URL endpoint: {api_path} ')
        print(f'{response.access_control_allow_origin}')

        return iterator

"""
app = create_app('../config_dev.toml')
#app.json = ImprovedJsonProvider(app)
#app.wsgi_app = AppMiddleware(app.wsgi_app)

#CORS(app, resources={r"/*":{'origins':"*"}})
#CORS(app, supports_credentials=True, origins=["http://localhost:5174"])

"""
@app.before_request
def before_request_func():
    print('In Before_request')
    api_method = request.method
    if api_method in ['POST', 'PUT', 'PATCH']:
        if request.json == '' or request.json == None:
            abort(500, description="request body is empty")
    api_endpoint_func = request.endpoint
    api_path = request.path
    app.logger.info(f'accessing URL endpoint: {api_path}, function name: {api_endpoint_func} ')

@app.after_request
def after_request_func(response:Response):
    print('In After_request')
    api_endpoint_func = request.endpoint
    api_path = request.path
    resp_allow_origin = response.access_control_allow_origin
    app.logger.info(f"access_control_allow_origin header: {resp_allow_origin}")
    app.logger.info(f'exiting URL endpoint: {api_path}, function name: {api_endpoint_func} ')
    return response
"""

@app.before_request
def log_session_cookie():
    print(">>> Print all cookies:", request.cookies)
    print(">>> Raw session cookie from client:", request.cookies.get('session'))
    print(">>> Decoded session object:", dict(session))  # shows current session data

@app.after_request
def add_csp_header(response:Response):
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:;"
    response.headers['X-Frame-Options'] = 'DENY'
    return response


if __name__ == "__main__":
    app.run(debug=True, port=5005)