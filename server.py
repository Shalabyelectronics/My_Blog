from flask import Flask, render_template
import requests
from post import Post

app = Flask(__name__)

response = requests.get("https://api.npoint.io/bdc8bdc56678a468c5cd")
post_data = response.json()
posts = []
for post in post_data:
    posts.append(Post(p_id=post["id"], p_title=post["title"],
                      p_subtitle=post["subtitle"], p_body=post["body"],
                      p_author=post["author"], p_date=post["date"]))


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


@app.route("/contact")
def get_contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)
