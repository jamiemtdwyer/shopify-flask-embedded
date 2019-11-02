# shopify-flask-embedded

This is an example Shopify application written in Python with Flask which authenticates with Shopify via OAuth, performs authenticated API requests, and initializes the Shopify App Bridge library.

## Getting started

1. Create a new Shopify application from the [Shopify Partner Dashboard](https://partners.shopify.com).
2. In the root folder of the project, create a new file named `.env` or copy the provided sample (`cp sample.env .env`)
3. Add your API key and secret key (from the Shopify Partner Dashboard) to the `.env` file.
4. Install the requirements for this project via pip (`pip install -r requirements.txt`)
5. Run the project with `env FLASK_APP=shopify_flask.py flask run`

7. Navigate to the application in your browser, supplying the domain of your Shopify store as the `shop` query parameter (`https://22638980.ngrok.io/?shop=my-shop.myshopify.com`)

NOTE: This app assumes that it is running over HTTPS - the easiest way to achieve this is by using a tunneling service like [ngrok](https://ngrok.com)

Make sure to enable third-party cookies in your browser! Some browsers such as Safari and Chromium block third-party cookies by default.
