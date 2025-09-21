from ippanel import Client
from online_shop import settings
import os
import requests
import json
"""
def send_verification_code(phone_number, code):
    api = kavenegar.KavenegarAPI(settings.KAVENEGAR_API_KEY)
    params = {
        'sender': '1000596446',  # Your Kavenegar sender number
        'receptor': phone_number,
        'message': f'Your verification code is: {code}',
    }
    api.sms_send(params)
"""




def send_verification_code(phone_number, code):
    API_KEY = os.getenv('API_KEY')

    url = "https://edge.ippanel.com/v1/api/send"

    print(phone_number , code)
          
    payload = json.dumps({
      "sending_type": "pattern",
      "from_number": "+9810004223",
      "code": "0s4osu9wi3ekzsv",
      "recipients": [
        str(phone_number)
      ],
      "params": {
        "code": str(code)
      }
    })
    
    # {"sending_type": "pattern", "from_number": "+9810004223", "code": "0s4osu9wi3ekzsv", "recipients": ["+9809103799860"], "params": {"code": "8181"}}
    # {"sending_type": "pattern", "from_number": "+9810004223", "code": "0s4osu9wi3ekzsv", "recipients": ["+989103799860"], "params": {"code": "7181"}}
    headers = {
  'Authorization': API_KEY,
  'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)








