import cv2
from uuid import uuid4
from flask import Flask, render_template, request, url_for, redirect
from dotenv import load_dotenv
from .linepay import LinePay

app = Flask(__name__)


@app.route("/online-pay")
def online_pay():
    capture = request.args.get("capture")
    request_options = {
        "amount": 300,
        "currency": "TWD",
        "orderId": str(uuid4()),
        "packages": [
            {
                "id": "20220314I001",
                "amount": 300,
                "name": "中山店",
                "products": [
                    {"name": "商品1", "quantity": 1, "price": 150},
                    {"name": "商品2", "quantity": 1, "price": 150},
                ],
            }
        ],
        "redirectUrls": {
            "confirmUrl": url_for("online_pay_confirm", _external=True),
            # "confirmUrlType": "SERVER",
            "cancelUrl": "https://pay.line.me/portal/tw/main",
        },
        "options": {"payment": {"capture": False if capture == "false" else True}},
    }

    linepay = LinePay()
    linepay_response = linepay.api_v3("post", "/v3/payments/request", request_options)
    print(linepay_response.json())
    return render_template(
        "online-pay.html", url=linepay_response.json()["info"]["paymentUrl"]["web"]
    )


@app.route("/online-pay/confirm")
def online_pay_confirm():
    print(request.args)
    print(request.data)
    transaction_id = request.args.get("transactionId")
    order_id = request.args.get("orderId")
    if transaction_id:
        linepay = LinePay()
        linepay_response = linepay.api_v3(
            "post",
            "/v3/payments/" + transaction_id + "/confirm",
            {"amount": 300, "currency": "TWD"},
        )
        print(linepay_response.json())
    return "OK", 200


@app.route("/online-pay/refund/<transaction_id>")
def online_pay_refund(transaction_id):
    linepay = LinePay()
    linepay_response = linepay.api_v3(
        "post", "/v3/payments/" + transaction_id + "/refund", {}
    )
    print(linepay_response.json())
    return "OK", 200


@app.route("/qrcode")
def scan_qrcode():
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()
    _, img = cap.read()
    while True:
        _, img = cap.read()
        data, bbox, _ = detector.detectAndDecode(img)
        if data:
            break
    cap.release()
    cv2.destroyAllWindows()
    return redirect(url_for("offline_pay", one_time_key=data, _external=True))


@app.route("/offline-pay/<one_time_key>")
def offline_pay(one_time_key):
    request_options = {
        "productName": "商品1*1;商品2*1",
        "amount": 300,
        "currency": "TWD",
        "orderId": str(uuid4()),
        "oneTimeKey": one_time_key,
        "capture": True,
        "extras": {
            "branchName": "中山店",
            "branchId": "20220314I001",
        },
    }

    linepay = LinePay()
    linepay_response = linepay.api_v2(
        "post", "/v2/payments/oneTimeKeys/pay", request_options
    )
    print(linepay_response.json())
    return "OK"


if __name__ == "__main__":
    load_dotenv()
    app.run(debug=True, port=5002)
