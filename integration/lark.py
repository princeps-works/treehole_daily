import logging
from requests_toolbelt import MultipartEncoder
import requests
import json
import os


def get_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = json.dumps({
        "app_id": os.environ.get('LARK_APP_ID'),
        "app_secret": os.environ.get('LARK_APP_SECRET')
    })

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200 and response.json()['code'] == 0 and response.json()['msg'] == 'ok':
        return response.json()['tenant_access_token']
    else:
        logging.error(response.text)
        return -1


def upload_image(img, token):
    url = "https://open.feishu.cn/open-apis/im/v1/images"
    form = {'image_type': 'message', 'image': img}
    multi_form = MultipartEncoder(form)
    headers = {
        'Content-Type': multi_form.content_type,
        'Authorization': f'Bearer {token}'
    }
    response = requests.request("POST", url, headers=headers, data=multi_form)
    if response.status_code == 200 and response.json()['code'] == 0 and response.json()['msg'] == 'success':
        return response.json()['data']['image_key']
    else:
        logging.error(response.text)
        return -1


def send_image(image_key, token):
    url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id"

    payload = json.dumps({
        "content": "{\"image_key\": \"" + image_key + "\"}",
        "msg_type": "image",
        "receive_id": os.environ.get('LARK_RECEIVE_ID')
    })

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200 and response.json()['code'] == 0 and response.json()['msg'] == 'success':
        logging.info(response.json()['msg'])
    else:
        logging.error(response.json()['msg'])


def send(img):
    token = get_token()
    assert token != -1
    img_key = upload_image(img, token)
    assert img_key != -1
    send_image(img_key, token)
