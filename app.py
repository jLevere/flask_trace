from flask import Flask, request, make_response, render_template
from flask_bootstrap import Bootstrap

import ipaddress
import json

'''
tldr: flask webapp that returns info about incoming request like headers and ip.  

This flask webapp echos information about incoming requests in different formats.  It returns the headers of incoming connections in plain text and json.  It also 
returns the seen ip of incoming connections in plain text.  It supports 'GET', 'POST', 'OPTIONS', 'TRACE' methods.  There isnt really any reason it cant support others,
just didnt think they would be used as much.  On reciving an unsupported method it returns an error message showing allowed methods.

'''

app = Flask(__name__)

bootstrap = Bootstrap(app)


# get remote address.
'''
Check if address is private, if it is, then its being proxied, so try to get the
real address.
'''
def try_for_real_ip(ip, headers):
    ip = str(ip)
    headers_dict = dict((headers).to_wsgi_list())

    if ipaddress.ip_address(ip).is_private and 'X-Forwarded-For' in headers_dict:
        ip = headers_dict['X-Forwarded-For']

    return ip

def build_resp(request, msg, response_code, content_type):

    response = make_response(msg, response_code)
    response.headers['Content-Type'] = content_type
    response.headers['Server'] = 'dont push it'
    response.headers['info'] = '/about'
    response.headers['remote_addr'] = try_for_real_ip(request.remote_addr, request.headers)

    return response

@app.route('/', methods=['GET', 'POST', 'OPTIONS', 'TRACE'])
def json_page():

    headers = dict((request.headers).to_wsgi_list())

    return build_resp(request, headers, 200, 'application/json')

@app.route('/headers/text')
def text_page():
    headers = dict((request.headers).to_wsgi_list())
    headers = str(json.dumps(headers, indent=4))

    return build_resp(request, headers, 200, 'text/plain; charset=utf-8')

@app.route('/ip')
def ip_page():

    ip = try_for_real_ip(request.remote_addr, request.headers)
    return build_resp(request, ip, 200, 'text/plain; charset=utf-8')

@app.route('/about')
def about_page():

    return build_resp(request, render_template('about.html'), 200, 'text/html; charset=utf-8')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(405)
def method_not_supported(e):

    error_msg =     '''
    {
        "error" : "http method not supported",
        "supported methods" : "GET, POST, OPTIONS, TRACE"
    }
    '''

    return build_resp(request, error_msg, 405, 'text/plain; charset=utf-8')

if __name__ == '__main__':
    app.run()
