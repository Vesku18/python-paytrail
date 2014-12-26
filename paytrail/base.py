# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
import hmac
import base64
import hashlib

from requests import Request

from paytrail.settings import BASE_API_URL, PAYTRAIL_AUTH_KEY, PAYTRAIL_ID, PAYTRAIL_SECRET


class PaytrailConnectAPIRequest(Request):
    def __init__(self, **kwargs):
        self.merchant_id = kwargs.pop('merchant_id')
        self.merchant_secret = kwargs.pop('merchant_secret')

        super(PaytrailConnectAPIRequest, self).__init__(**kwargs)

        self.headers['Timestamp'] = self.get_timestamp()
        self.headers['Content-MD5'] = self.get_content_md5()
        self.headers['Authorization'] = self.get_authorization_signature()

    def get_content_md5(self):
        return hashlib.md5(self.prepare().body).digest().encode('base64').strip()

    @staticmethod
    def get_timestamp():
        return str(datetime.now().isoformat())

    def get_authorization_signature(self):
        base_signature = '\n'.join([
            self.method,
            self.url,
            'PaytrailConnectAPI {merchant_id}'.format(self.merchant_id),
            self.headers['Timestamp'],
            self.headers['Authorization']
        ])

        digest = hmac.new(
            key=self.merchant_secret,
            msg=base_signature,
            digestmod=hashlib.sha256
        ).digest()

        signature = base64.b64encode(digest).decode()
        return 'PaytrailConnectAPI {merchant_id}:{signature}'.format(self.merchant_id, signature)


class BasePaytrailClient(object):
    URL_MAP = {
        'authorization':
            {
                'url': '/connectapi/authorizations',
                'method': 'POST'
            },
        'confirming_authorization':
            {
                'url': '/connectapi/authorizations/{id}/confirmation',
                'method': 'POST'
            },
        'invalidatin_authorization':
            {
                'url': '/authorizations/{id}',
                'method': 'POST'
            }
        ,
        'charging': '/connectapi/authorizations/{id}/charges',
        'fetching_payment_status': '/connectapi/authorizations/{id}/charges/{id}',
        'fetching_delivery_address': ' /connectapi/authorizations/{id}/deliveryAddresses',
    }

    def __init__(self, base_url=BASE_API_URL, merchant_id=PAYTRAIL_ID, merchant_secret=PAYTRAIL_SECRET):
        self.base_url = base_url
        self.merchant_id = merchant_id
        self.merchant_secret = merchant_secret

    def authorize(self, auth_key=PAYTRAIL_AUTH_KEY):
        pass

    def confirm_authorization(self):
        pass


test_client = BasePaytrailClient()

test_client.authorize()