from flask import Flask, request, make_response, render_template
from flask_bootstrap import Bootstrap

import json
app = Flask(__name__)

bootstrap = Bootstrap(app)

@app.route('/headers/json')
def json_page():

    headers = dict((request.headers).to_wsgi_list())
   
    response = make_response(headers, 200)
    response.headers['Content-Type'] = 'application/json'
    response.headers['Server'] = 'dont push it'
    response.headers['info'] = 'link_to_info_page'
    response.headers['remote_addr'] = request.remote_addr

    return response

@app.route('/headers')
def text_page():
    headers = dict((request.headers).to_wsgi_list())
    headers = str(json.dumps(headers, indent=4))

    response = make_response(headers, 200)
    response.headers['Content-Type'] = 'text/plain; charset=utf-8'
    response.headers['Server'] = 'dont push it'
    response.headers['info'] = 'link_to_info_page'
    response.headers['remote_addr'] = request.remote_addr

    return response

@app.route('/ip')
def ip_page():
    ip_addr = str(request.remote_addr)

    response = make_response(ip_addr, 200)
    response.headers['Content-Type'] = 'text/plain; charset=utf-8'
    response.headers['Server'] = 'dont push it'
    response.headers['info'] = 'link_to_info_page'
    response.headers['remote_addr'] = request.remote_addr

    return response

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run()
