import requests
import json

def get_access_token(app_key, app_secret):
    url = f"https://oapi.dingtalk.com/gettoken?appkey={app_key}&appsecret={app_secret}"
    response = requests.get(url)
    result = response.json()
    return result["access_token"]

def send_private_message(access_token, robot_code, user_id, msg_key, msg_param):
    url = "https://api.dingtalk.com/v1.0/robot/oToMessages/batchSend"
    headers = {
        "x-acs-dingtalk-access-token": access_token,
        "Content-Type": "application/json"
    }
    data = {
        "robotCode": robot_code,
        "userIds": [user_id],
        "msgKey": msg_key,
        "msgParam": json.dumps(msg_param)
    }
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    return result

if __name__ == "__main__":
    app_key = "YOUR_APP_KEY"
    app_secret = "YOUR_APP_SECRET"
    robot_code = "YOUR_ROBOT_CODE"
    user_id = "YOUR_USER_ID"
    msg_key = "sampleMarkdown"
    msg_param = {
        "text": "hello text",
        "title": "hello title"
    }

    access_token = get_access_token(app_key, app_secret)
    result = send_private_message(access_token, robot_code, user_id, msg_key, msg_param)
    print(result)

