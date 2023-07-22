import os
import json
import requests
from uuid import uuid4
from .signature import get_auth_signature


class LinePay:
    def __init__(self):
        self._headers = {
            "Content-Type": "application/json",
            "X-LINE-ChannelId": os.environ.get("CHANNEL_ID"),
        }
        self._secret = os.environ.get("CHANNEL_SECRET")

    def api_v3(self, method, uri, payload):
        json_body = json.dumps(payload)
        nonce = str(uuid4())
        self._headers.update({"X-LINE-Authorization-Nonce": nonce})
        self._headers["X-LINE-Authorization"] = get_auth_signature(
            self._secret, uri, json_body, nonce
        )
        response = getattr(requests, method)(
            os.environ.get("LINEPAY_ENDPOINT") + uri,
            headers=self._headers,
            data=json_body,
        )
        return response

    def api_v2(self, method, uri, payload):
        self._headers["X-LINE-ChannelSecret"] = self._secret
        json_body = json.dumps(payload)
        print(json_body)
        response = getattr(requests, method)(
            os.environ.get("LINEPAY_ENDPOINT") + uri,
            headers=self._headers,
            data=json_body,
        )
        return response
