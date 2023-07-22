import base64
import hmac
import hashlib


def get_auth_signature(secret, uri, body, nonce):
    """
    用於製作密鑰
    :param secret: your channel secret
    :param uri: uri
    :param body: request body
    :param nonce: uuid or timestamp(時間戳)
    :return:
    """
    str_sign = secret + uri + body + nonce
    return base64.b64encode(
        hmac.new(
            str.encode(secret), str.encode(str_sign), digestmod=hashlib.sha256
        ).digest()
    ).decode("utf-8")
