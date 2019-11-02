from flask import Flask, redirect, render_template, request, session, url_for
from pyactiveresource.connection import UnauthorizedAccess
import shopify
import os
import binascii
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Generate a random key for signing the session:
app.secret_key = binascii.hexlify(os.urandom(16))

# API credentials are sourced from enviroment variables:
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
API_VERSION = '2019-10'
shopify.Session.setup(api_key=API_KEY, secret=API_SECRET)


@app.route('/')
def index():
    if not is_authenticated():
        return login()

    api_session = shopify.Session(
        session['shop'],
        API_VERSION,
        session['access_token'])

    shopify.ShopifyResource.activate_session(api_session)

    try:
        products = shopify.Product.find(limit=10)
    except UnauthorizedAccess:
        return login()
    except:
        return "An unknown error occured.", 500

    return render_template('products.html', api_key=API_KEY, products=products)


@app.route('/auth/shopify/callback')
def oauth_callback():
    params = request.args
    shop = params['shop']

    try:
        token = shopify.Session(shop, API_VERSION).request_token(params)
    except shopify.session.ValidationException:
        return "HMAC signature does not match. Check your API credentials.", 400
    except:
        return "An unknown error occured.", 500

    session['shop'] = shop
    session['access_token'] = token

    return redirect(url_for('index'))


def is_authenticated():
    params = request.args
    if ('shop' in params) & ('shop' in session):
        if session['shop'] != params['shop']:
            clear_session()
            return False

    return 'access_token' in session


def clear_session():
    del session['shop']
    del session['access_token']


def login():
    scopes = ['read_products']

    shop = request.args.get('shop', None)
    if shop is not None:
        return render_template(
            'login.html',
            shop=shop,
            api_key=API_KEY,
            scopes=','.join(scopes),
            redirect_uri=url_for('oauth_callback', _external=True, _scheme='https'))

    else:
        return "No shop parameter provided.", 400
