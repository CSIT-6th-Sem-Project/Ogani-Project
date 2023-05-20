from django.shortcuts import render

# Create your views here.
import requests,json
from store.views import BaseView
from django.views.generic import FormView
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .forms import OrderForm
from .models import *
from django.http.response import JsonResponse,HttpResponseBadRequest,HttpResponse
from Organi import settings
from cart_app.models import Cart



class CartCheckoutView(BaseView,FormView):
    form_class = OrderForm
    template_name = "checkout.html"

    def get_context_data(self, *args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        self.view
        self.view['Carts'] = Cart.objects.filter(user=self.request.user,checkout = False)
        self.view['Shipping'] = Order.SHIPPING
        context.update(self.view)
        return context

    def form_valid(self, form):
        f_name,l_name = form.cleaned_data.get('first_name'),form.cleaned_data.get('last_name')
        email,phone = form.cleaned_data.get('email'),form.cleaned_data.get('phone')
        city,address = form.cleaned_data.get('city'),form.cleaned_data.get('address')
        shipping_address = form.cleaned_data.get('shipping_address')
        order_notes = form.cleaned_data.get('order_notes')
        payment_type = form.cleaned_data.get('payment_type')

        order_obj = Order.objects.create(
            user = self.request.user,
            first_name = f_name,
            last_name = l_name,
            email = email,
            phone = phone,
            city = city,
            address = address,
            shipping_address  = shipping_address,
            order_notes= order_notes,
            payment_type = payment_type
        )

        order_obj.save()
        for cart in Cart.objects.filter(user=self.request.user,checkout=False):
            order_items = OrderItem.objects.create(order = order_obj,product = cart.product,price = cart.total , quantity = cart.quantity)
            order_items.save()
            # set all cart items checkout to True
            cart.checkout = True
            cart.save()



        if (payment_type == Order.EPAYMENT):
            messages.success(self.request, "Order Placed Successfully ... you can now pay via khalti")
            return redirect(f"/payment/khalti-payment/{order_obj.slug}")
        elif(payment_type==Order.CASH_ON_DELIVERY):
            messages.info(self.request,"Order Placed Download the receipt for later transactions")
            return redirect(f"/payment/download-transaction-pdf?order_id={order_obj.slug}")


def khalti_payment(request,slug):
    view = BaseView.view
    # test public key necessary for performing transaction
    view["khalti_public_key"] = os.environ.get("KHALTI_TEST_PUBLIC_KEY")
    # get the recently created billing order
    order = get_object_or_404(Order,slug = slug)
    view['total_amount'] = order.total_payment * 100 # converting Rs to paisa
    view['order_slug'] = order.slug

    return render(request,'khaltipayment.html',view)

def verify_khalti_payment(request):
    # neccessary paramemters to send to verify payment to khalti
    verify_url = settings.KHALTI_API_URL
    private_key = os.environ.get("KHALTI_TEST_SECRET_KEY")
    headers = {"Authorization": f"Key {private_key}"}
    if (request.method == "POST"):

        token = request.POST['token']
        amount = request.POST['amount'],
        order_slug = request.POST['order_slug']
        payload ={'token':token,'amount':amount}

        # send server to server verification requests
        resp = requests.request("POST",verify_url,headers=headers,data=payload)
        print(resp.content)
        if(resp.status_code == 200):
            # converting the obtained khalti json response to dictionary
            resp = resp.content.decode()
            transaction = json.loads(resp)
            # if Transaction state is completed do this
            if(transaction['state']['name']=="Completed"):
                messages.success(request,"Transaction Completed Successfully...please save the receipt")
                # set the bill  state to paid
                bill = get_object_or_404(Order,slug=order_slug)
                bill.paid = True
                bill.save()

                # save json transaction obtained from khalti after successfull transaction
                khalti_transaction = KhaltiTransactionRecord.objects.create(user=request.user,transaction=resp)
                khalti_transaction.save()
                return JsonResponse({'message':"Transaction Completed Successfully","success":True})
            # if transaction is in other states rather than completed
            else:
                messages.info(request,f"Transaction is in {transaction['state']['name']} ... please wait")
                return JsonResponse({"message":f"Transaction is in {transaction['state']['name']} ... Please Wait !!","success":False})
        # in case for failed Transactions
        else:
            messages.error(request,"Transaction Failed ... Please Try Again !!")
            return JsonResponse({"message":"Transaction Failed ... Please Try Again !!","success":False})

    # If other Requests are performed
    messages.error(request,"Invalid Request")
    return HttpResponseBadRequest("Bad Gateway!!")

def download_transaction_pdf(request):

    context = BaseView.view
    slug = request.GET['order_id']
    order = get_object_or_404(Order, user=request.user, slug=slug)
    ordered_items = OrderItem.objects.filter(order=order)
    context.update({'ordered_items': ordered_items, 'order': order, 'total_amount': order.total_payment,
               'shipping': Order.SHIPPING})

    return render(request,"download-transaction-pdf.html",context)

def generate_transaction_pdf(request,slug):
    template_path = 'generate-transaction-pdf.html'

    order = get_object_or_404(Order,user = request.user,slug=slug)

    ordered_items = OrderItem.objects.filter(order = order)

    context = {'ordered_items': ordered_items,'order':order,'total_amount':order.total_payment,'shipping': Order.SHIPPING}


    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')

    # to directly download the pdf we need attachment
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    # to view on browser we can remove attachment
    response['Content-Disposition'] = f'filename="khalti-transaction-{slug}-report.pdf"'

    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response
    )
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


