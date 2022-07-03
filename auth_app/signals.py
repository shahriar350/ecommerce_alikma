import datetime

import requests
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from auth_app.models import UserOTP


@receiver(post_save, sender=UserOTP)
def update_stock(sender, instance, **kwargs):
    data = {
        "trxID": str(instance.id),
        "trxTime": instance.date_created.strftime('%Y-%m-%d %H:%M:%S'),
        "smsDatumArray": [
            {
                "smsID": str(instance.id),
                "smsSendTime": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "mobileNo": "{0}{1}".format("88",instance.phone_number),
                "smsBody": "Your {0}\'s website otp is: {1}".format(settings.WEBSITE_NAME,instance.otp)
            }
        ]
    }
    url = "https://api.infobuzzer.net/v3.1/SendSMS/sendSmsInfoStore"
    r = requests.post(
        url=url, json=data, auth=(settings.OTP_USERNAME,settings.OTP_PASSWORD),headers={
            'Content-Type': 'application/json'
        }
    )
