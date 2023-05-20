
var btn = document.getElementById("payment-button");
var span_text = document.getElementById("payment-btn-span");
var spinner = document.getElementById("spinner");
var total_amount = Number(document.getElementById("total_amount").value);
span_text_txt = "Pay via Khalti Rs."+(total_amount/100);


var config = {

            "publicKey": document.getElementById('public_key').value,
            "productIdentity": document.getElementById('productIdentity').value,
            "productName": "Ogani Products",
            "productUrl": "http://localhost:8000/",
            "paymentPreference": ["KHALTI"],
            "eventHandler": {
                onSuccess (payload) {
                    $("#payment-btn-span").text("Verifying Payment ...");
                    $("#spinner").css("display","inline-block");
                    $.ajax({
                    method: "POST",
                    url:"/payment/verify-khalti-payment",
                    data:{
                        token: payload.token,
                        amount: payload.amount,
                        order_slug:$("#productIdentity").val(),
                        csrfmiddlewaretoken:$("input[name='csrfmiddlewaretoken']").val()
                    },success: function (data){
                        console.log(data)
                        if (data.success){
                            window.location = "http://localhost:8000/payment/download-transaction-pdf?order_id="+document.getElementById('productIdentity').value;
                        }else{
                            window.location="http://localhost:8000/payment/khalti-payment"
                        }
                    },
                    error: function (data){
                        console.log(data)
                    }
                    });
                },
                onError (error) {
                    spinner.style.display = "none";
                    span_text.innerHtml = "Some Error Occurred !!"
                    span_text.style.color = "red";
                },
                onClose () {
                    console.log('widget is closing');
                    spinner.style.display = "none";
                    span_text.innerHtml = span_text_txt;
                }
            }
        };
var checkout = new KhaltiCheckout(config);
btn.onclick = function () {
            // minimum transaction amount must be 10, i.e 1000 in paisa.

            checkout.show({amount: 200*100});
            span_text.innerHtml = "Processing Payment";
            spinner.style.dispay="inline-block"

}
