from flask import *
import sqlite3

app = Flask(__name__)
app.secret_key = "WhyNotSetTheSecretKeyToSarina?"

def connect_to_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = connect_to_db()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

@app.route("/")
def index():
    conn = connect_to_db()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

if __name__ == "__main__":
    app.run(debug=True, port=12345)
