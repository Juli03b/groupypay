import os
from flask import Flask
from flask.json import jsonify
import stripe

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'its_a_secret')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///groupypay')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
stripe.api_key = 'sk_test_51JcbCnEZzJXhLfiIMZpV7PrwHj2Os7rNTNq1jR8h3WPcOTBuKfE5pjzKsYEC2uyEaPXzmi8jVjZ0Yg46E94Y7wKP00OCM2bRPi'

@app.route("/")
def home():
    account_one = stripe.Account.create(
    type="express",
    country="US",
    email="jenny.rosen@example.com",
    capabilities={
        "card_payments": {"requested": True},
        "transfers": {"requested": True},
    },)
    account_two = stripe.Account.create(
    type="express",
    country="US",
    email="jenny.rosen@example.com",
    capabilities={
        "card_payments": {"requested": True},
        "transfers": {"requested": True},
    },)
    account_links = stripe.AccountLink.create(
      account=account_one.id,
      refresh_url='https://localhost:5000/reauth',
      return_url='https://localhost:5000/',
      type='account_onboarding',
    )
    payment = stripe.PaymentIntent.create(
      amount=12,
      currency='usd',
      application_fee_amount=10,
      payment_method_types=['card'],
      on_behalf_of=f'{account_one.id}',
      transfer_data={
        'destination': f'{account_two.id}',
      },
    )
    return jsonify(account_one, account_links, payment)
