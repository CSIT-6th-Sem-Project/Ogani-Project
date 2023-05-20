from django.urls import path

from .views import *

# View For Handling Payment Related Operations

urlpatterns = [

    path("cart-checkout",CartCheckoutView.as_view(),name="cart_checkout"),

    path('khalti-payment/<slug>',khalti_payment,name="khalti_payment"),

    path('verify-khalti-payment',verify_khalti_payment,name="verify_khalti_payment"),

    path('generate-transaction-pdf/<slug>',generate_transaction_pdf,name="generate_transaction_pdf"),

    path('download-transaction-pdf',download_transaction_pdf,name="download_transaction_pdf")
]