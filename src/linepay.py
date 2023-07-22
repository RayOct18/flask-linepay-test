import os
import json
import requests
from uuid import uuid4
from .signature import get_auth_signature


class LinePay:
    def __init__(self):
        self._headers = {
            'Content-Type': 'application/json',
            'X-LINE-ChannelId': os.environ.get('CHANNEL_ID'),
            'X-LINE-Authorization-Nonce': str(uuid4()),
        }
        self._secret = os.environ.get('CHANNEL_SECRET')
    
    def request(
            self,
            method,
            uri,
            payload
    ):
        json_body = json.dumps(payload)
        self._headers['X-LINE-Authorization'] = get_auth_signature(
            self._secret,
            uri,
            json_body,
            self._headers['X-LINE-Authorization-Nonce']
        )
        response = getattr(requests, method)(
            os.environ.get('LINEPAY_ENDPOINT') + uri,
            headers=self._headers,
            data=json_body
        )
        return response
