import os
from flask import *
import sqlite3

USERNAME = "Ali"
PASSWORD = "pass"

# Make the app and set the Secret Key
app = Flask(__name__)
app.secret_key = "WhyNotSetTheSecretKeyToSarina?"

# A function for connecting to the database and getting the database object
def connect_to_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# A function to get a post with it's ID
def get_post(post_id):
    conn = connect_to_db()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

# If a user goes to https://name.com/ it will return the html
@app.route("/")
def index():
    # Recieving all the posts
    conn = connect_to_db()
    sqlposts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    # Putting all the posts in a list
    posts = []
    for post in sqlposts:
        posts.append(post)
        
    # Getting the last 3 posts
    posts3 = []
    if len(posts) >= 3:
        posts3.append(posts[len(posts)-1])
        posts3.append(posts[len(posts)-2])
        posts3.append(posts[len(posts)-3])
    elif len(posts) == 2:
        posts3.append(posts[len(posts)-1])
        posts3.append(posts[len(posts)-2])
    elif len(posts) == 1:
        posts3.append(posts[len(posts)-1])
        
    # Rendering the main page and sending the last 3 posts to it
    return render_template('index.html', posts=posts3)

# If a user goes to https://name.com/posts it will return the html
@app.route("/posts")
def posts():
    # Recieving all the posts
    conn = connect_to_db()
    posts_list = conn.execute('SELECT * FROM posts').fetchall()
    # Reversing the list items
    posts_list = posts_list[::-1]
    conn.close()
    # Render the html
    return render_template("posts.html", posts=posts_list)

@app.route("/staff", methods = ['GET', 'POST'])
def staff():
    return render_template("staff.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    msg = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and PASSWORD == "pass":
            
            session["loggedin"] = True
            session["id"] = "1"
            session["username"] = "Admin"
            
            return redirect(url_for("index"))
        else:
            msg = "نام کاربری یا رمز عبور اشتباه است !"
        
    return render_template("login.html", msg=msg)

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for("index"))

@app.route("/create", methods=["GET", "POST"])
def create():
    msg = ""
    if request.method == "POST" and "title" in request.form and "content" in request.form:
        title = request.form["title"]
        content = request.form["content"]
        img = request.files["img"]
        img_a = None
        if img:
            img_a = f"{img.filename}"
            img.save(f"static/user_images/{img.filename}")
        conn = connect_to_db()
        conn.execute("INSERT INTO posts (img, title, content) VALUES (?, ?, ?)", (img_a, title, content))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
        
    elif request.method == "POST":
        msg = "Please fill out the form !"
    
    return render_template("create.html", msg=msg)

@app.route("/edit/<idd>", methods=["POST", "GET"])
def edit(idd):
    post = get_post(idd)
    conn = connect_to_db()
    if request.method == "POST" and "title" in request.form and "content" in request.form:
        title = request.form["title"]
        content = request.form["content"]
        img = request.files["img"]
        ali = conn.execute("SELECT * FROM posts").fetchall()
        
        if img.filename == "":
            img = post["img"]
            conn.execute("UPDATE posts SET title=?, content=? WHERE id=?", (title, content, idd))
        else:
            img.save(f"static/user_images/{img.filename}")
            conn.execute("UPDATE posts SET img=?, title=?, content=? WHERE id = ?", (img.filename, title, content, idd))
            
            
        
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template("edit.html", post=post)

@app.route("/delete/<idd>")
def delete(idd):
    post = get_post(idd)
    #old_img = post["img"]
    #os.remove(f"static/user_images/{old_img}")
    conn = connect_to_db()
    conn.execute('DELETE FROM posts WHERE id = ?', (idd))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=12345)
