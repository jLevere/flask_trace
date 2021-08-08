from flask import Flask, request, make_response, render_template
from flask_bootstrap import Bootstrap

import ipaddress

import json
app = Flask(__name__)

bootstrap = Bootstrap(app)



# get remote address.
'''
Check if address is private, if it is, then its being proxied, so try to get the
real address.
'''
def try_for_real_ip(ip, headers):
    print(ip)
    ip = str(ip)
    headers_dict = dict((headers).to_wsgi_list())

    if ipaddress.ip_address(ip).is_private and 'X-Forwarded-For' in headers_dict:
        ip = headers_dict['X-Forwarded-For']
        print(ip)

    return ip

@app.route('/', methods=['GET', 'POST', 'OPTIONS', 'TRACE'])
def json_page():

    headers = dict((request.headers).to_wsgi_list())
   
    response = make_response(headers, 200)
    response.headers['Content-Type'] = 'application/json'
    response.headers['Server'] = 'dont push it'
    response.headers['info'] = '/about'
    response.headers['remote_addr'] = try_for_real_ip(request.remote_addr, request.headers)

    return response

@app.route('/headers/text')
def text_page():
    headers = dict((request.headers).to_wsgi_list())
    headers = str(json.dumps(headers, indent=4))

    response = make_response(headers, 200)
    response.headers['Content-Type'] = 'text/plain; charset=utf-8'
    response.headers['Server'] = 'dont push it'
    response.headers['info'] = '/about'
    response.headers['remote_addr'] = try_for_real_ip(request.remote_addr, request.headers)

    return response

@app.route('/ip')
def ip_page():

    response = make_response(try_for_real_ip(request.remote_addr, request.headers), 200)
    response.headers['Content-Type'] = 'text/plain; charset=utf-8'
    response.headers['Server'] = 'dont push it'
    response.headers['info'] = '/about'
    response.headers['remote_addr'] = try_for_real_ip(request.remote_addr, request.headers)
    return response

@app.route('/about')
def about_page():
    response = make_response(render_template('about.html'), 200)
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    response.headers['Server'] = 'dont push it'
    response.headers['info'] = '/about'
    response.headers['remote_addr'] = try_for_real_ip(request.remote_addr, request.headers)
    return response


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
    response = make_response(error_msg, 200)
    response.headers['Content-Type'] = 'text/plain; charset=utf-8'
    response.headers['Server'] = 'dont push it'
    response.headers['info'] = '/about'
    response.headers['remote_addr'] = try_for_real_ip(request.remote_addr, request.headers)

    return response, 405

if __name__ == '__main__':
    app.run()
