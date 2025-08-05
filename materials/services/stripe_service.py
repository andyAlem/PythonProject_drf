import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(name):
    """Создание продукта в Stripe"""
    return stripe.Product.create(name=name)


def create_stripe_price(product_id, amount):
    """Создание цены в Stripe"""
    unit_amount = int(amount * 100)
    return stripe.Price.create(
        unit_amount=unit_amount, currency="rub", product=product_id
    )


def create_checkout_session(price_id, success_url, cancel_url):
    """Создание сессии оплаты в Stripe"""
    return stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url,
    )
