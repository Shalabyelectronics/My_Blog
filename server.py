from flask import Flask, render_template, request
import requests
from post import Post
import os
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

# Email information

SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
SENDER_PASS = os.environ.get("SENDER_PASS")
RECIPIENT_EMAIL = os.environ.get("SENDER_EMAIL")
# Add your email smtp server and port
SMTP_SERVER_PROVIDER = "smtp.gmail.com"
SMTP_PORT = 465

# request blog data
response = requests.get("https://api.npoint.io/bdc8bdc56678a468c5cd")
post_data = response.json()
posts = []
for post in post_data:
    posts.append(Post(p_id=post["id"], p_title=post["title"],
                      p_subtitle=post["subtitle"], p_body=post["body"],
                      p_author=post["author"], p_date=post["date"]))


def send_email(func):
    def wrapper(content):
        message_data = func(content)
        msg = EmailMessage()
        msg["Subject"] = "You Got New message💬"
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECIPIENT_EMAIL
        msg.set_content(message_data['content'])
        try:
            with smtplib.SMTP_SSL(SMTP_SERVER_PROVIDER, SMTP_PORT) as connection:
                connection.login(SENDER_EMAIL, SENDER_PASS)
                connection.send_message(msg)
                status = "Message sent"
        except Exception as r:
            return f"We could not send the message because of error {r} "
        else:
            return status
    return wrapper


@send_email
def collect_usr_data(content) -> dict:
    """This function collect user data to send a message"""
    return {'content': content}


@app.route("/")
def home_page():
    return render_template('index.html', all_posts=posts)


@app.route("/<int:post_id>")
def get_post(post_id):
    requested_blog = None
    for post in posts:
        if post.post_id == post_id:
            requested_blog = post
    return render_template('post.html', p=requested_blog)


@app.route("/about")
def get_about():
    return render_template('about.html')


@app.route("/contact", methods=["POST", "GET"])
def get_contact():
    return render_template('contact.html')


@app.route("/send_message", methods=["POST", "GET"])
def message_state():
    if request.method == "POST":
        collect_usr_data(content=f'Hello Shalaby you got a new message from your blog\n'
                                 f'name: {request.form.get("usr_name")}\n'
                                 f'email: {request.form.get("usr_email")}\n'
                                 f'phone: {request.form.get("usr_phone")}\n'
                                 f'message: {request.form.get("usr_message")}')
    return "<h1>Message sent</h1>"


if __name__ == '__main__':
    app.run(debug=True)
