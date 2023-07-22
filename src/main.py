from uuid import uuid4
from flask import Flask, render_template, request
from dotenv import load_dotenv
from .linepay import LinePay

app = Flask(__name__)

@app.route('/online-pay')
def online_pay():
    capture = request.args.get('capture')
    request_options = {
        "amount": 300,
        "currency": 'TWD',
        "orderId": str(uuid4()),
        "packages": [{
            "id": '20220314I001',
            "amount": 300,
            "name": '中山店',
            "products": [{
                "name": '商品1',
                "quantity": 1,
                "price": 150
            },{
                "name": '商品2',
                "quantity": 1,
                "price": 150
            }]
        }],
        "redirectUrls": {
            "confirmUrl": "https://67b6-123-241-167-212.ngrok-free.app/online-pay/confirm",
            # "confirmUrlType": "SERVER",
            "cancelUrl": 'https://fastapi.tiangolo.com/zh/tutorial/bigger-applications/'
        },
        "options": {
            "payment": {
                "capture": False if capture == 'false' else True
            }
        }
    }

    linepay = LinePay()
    linepay_response = linepay.request('post', '/v3/payments/request', request_options)
    print(linepay_response.json())
    return render_template("online-pay.html", url=linepay_response.json()['info']['paymentUrl']['web'])

@app.route('/online-pay/confirm')
def online_pay_confirm():
    print(request.args)
    print(request.data)
    transaction_id = request.args.get('transactionId')
    order_id = request.args.get('orderId')
    if transaction_id:
        linepay = LinePay()
        linepay_response = linepay.request('post', '/v3/payments/' + transaction_id + '/confirm', {
            "amount": 300,
            "currency": 'TWD'
        })
        print(linepay_response.json())
    return 'OK', 200

@app.route('/online-pay/refund/<transaction_id>') 
def online_pay_refund(transaction_id):
    linepay = LinePay()
    linepay_response = linepay.request('post', '/v3/payments/' + transaction_id + '/refund', {})
    print(linepay_response.json())
    return 'OK', 200


if __name__ == "__main__":
    load_dotenv()
    app.run(debug=True, port=5002)
