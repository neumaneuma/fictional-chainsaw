# . venv/bin/activate
# export FLASK_APP=hello.py && export FLASK_ENV=development && python3 -m flask run

from flask import make_response
from flask import abort, redirect, url_for
from flask import request
from flask import render_template
from flask import Flask
from flask.helpers import url_for
from markupsafe import escape

app = Flask(__name__)


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % escape(username)


@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % escape(subpath)


@app.route('/')
def hello_world():
    # raise Exception("test")
    return 'Hello, World!'


# The canonical URL for the projects endpoint has a trailing slash. It’s similar to a folder in a file system. If you access the URL without a trailing slash, Flask redirects you to the canonical URL with the trailing slash.
@app.route('/projects/')
def projects():
    return 'The project page'


# The canonical URL for the about endpoint does not have a trailing slash. It’s similar to the pathname of a file. Accessing the URL with a trailing slash produces a 404 “Not Found” error. This helps keep URLs unique for these resources, which helps search engines avoid indexing the same page twice.
@app.route('/about')
def about():
    return 'The about page'


#  if no verb is specified, then only get is supported by default. If get Is specified then head and options are implicitly supported as well.
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()


# /
# /login
# /login?next=/
# /user/John%20Doe
with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe'))

#Basically you can completely ignore that this is the case unless you are doing something like unit testing. You will notice that code which depends on a request object will suddenly break because there is no request object. The solution is creating a request object yourself and binding it to the context. The easiest solution for unit testing is to use the test_request_context() context manager. In combination with the with statement it will bind a test request so that you can interact with it. Here is an example:
with app.test_request_context('/hello', method='POST'):
    # now you can do something with the request until the
    # end of the with block, such as basic assertions:
    assert request.path == '/hello'
    assert request.method == 'POST'


# The current request method is available by using the method attribute. To access form data (data transmitted in a POST or PUT request) you can use the form attribute. Here is a full example of the two attributes mentioned above:
# What happens if the key does not exist in the form attribute? In that case a special KeyError is raised. You can catch it like a standard KeyError but if you don’t do that, a HTTP 400 Bad Request error page is shown instead.
@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)


# To access cookies you can use the cookies attribute. To set cookies you can use the set_cookie method of response objects. The cookies attribute of request objects is a dictionary with all the cookies the client transmits. If you want to use sessions, do not use the cookies directly but instead use the Sessions in Flask that add some security on top of cookies for you.
# Reading cookies:
@app.route('/')
def index():
    username = request.cookies.get('username')
    # use cookies.get(key) instead of cookies[key] to not get a
    # KeyError if the cookie is missing.


# Storing cookies:
@app.route('/')
def index():
    resp = make_response(render_template(...))
    resp.set_cookie('username', 'the username')
    return resp


# To redirect a user to another endpoint, use the redirect() function; to abort a request early with an error code, use the abort() function:
@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


# This is a rather pointless example because a user will be redirected from the index to a page they cannot access (401 means access denied) but it shows how that works.
# By default a black and white error page is shown for each error code. If you want to customize the error page, you can use the errorhandler() decorator:
@app.errorhandler(404)
def page_not_found(error):
    return


# The return value from a view function is automatically converted into a response object for you. If the return value is a string it’s converted into a response object with the string as response body, a 200 OK status code and a text/html mimetype. If the return value is a dict, jsonify() is called to produce a response.
# You just need to wrap the return expression with make_response() and get the response object to modify it, then return it:


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404


@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('error.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp

# The attached logger is a standard logging Logger, so
app.logger.debug('A value for debugging')
app.logger.warning('A warning occurred (%d apples)', 42)
app.logger.error('An error occurred')