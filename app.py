import os
import json
from flask import Flask, request
from send_private_message import send_private_message, get_access_token
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

# 加载钉钉ID和GitHub ID映射关系表
with open("github_dingtalk_mapping.json", "r") as f:
    github_dingtalk_mapping = json.load(f)

app_key = os.getenv("YOUR_APP_KEY")
app_secret = os.getenv("YOUR_APP_SECRET")
robot_code = os.getenv("YOUR_ROBOT_CODE")
access_token = get_access_token(app_key, app_secret)

def handle_github_event(event, payload):
    msg_key = "sampleMarkdown"
    msg_param = None

    if event == "pull_request":
        pr_creator = payload["pull_request"]["user"]["login"]
        dingtalk_id = github_dingtalk_mapping.get(pr_creator)
        if dingtalk_id:
            msg_param = {
                "title": f"New PR created by {pr_creator}",
                "text": f"Title: {payload['pull_request']['title']}\nContent: {payload['pull_request']['body']}"
            }
    elif event == "issues":
        issue_creator = payload["issue"]["user"]["login"]
        dingtalk_id = github_dingtalk_mapping.get(issue_creator)
        if dingtalk_id:
            msg_param = {
                "title": f"New issue created by {issue_creator}",
                "text": f"Title: {payload['issue']['title']}\nContent: {payload['issue']['body']}"
            }
    elif event == "issue_comment":
        comment_creator = payload["comment"]["user"]["login"]
        dingtalk_id = github_dingtalk_mapping.get(comment_creator)
        if dingtalk_id:
            msg_param = {
                "title": f"New comment by {comment_creator}",
                "text": f"Comment: {payload['comment']['body']}"
            }
    elif event == "push":
        pusher = payload["pusher"]["name"]
        dingtalk_id = github_dingtalk_mapping.get(pusher)
        if dingtalk_id:
            commit_messages = "\n".join([f"{commit['author']['name']}: {commit['message']}" for commit in payload["commits"]])
            msg_param = {
                "title": f"New push by {pusher}",
                "text": f"Commit(s):\n{commit_messages}"
            }

    if dingtalk_id and msg_param:
        send_private_message(access_token, robot_code, dingtalk_id, msg_key, msg_param)


@app.route("/", methods=["POST"])
def webhook():
    event = request.headers.get("X-GitHub-Event")
    payload = request.get_json()
    handle_github_event(event, payload)
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0")

