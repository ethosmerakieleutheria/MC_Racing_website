# app/payment/stripe_config.py
import stripe
from ..config import settings

stripe.api_key = settings.stripe_secret_key

async def create_payment_intent(amount, currency="usd"):
    try:
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            payment_method_types=["card"],
        )
        return intent
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))