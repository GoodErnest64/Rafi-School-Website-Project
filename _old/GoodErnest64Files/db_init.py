import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

#cur.execute("INSERT INTO posts (img, title, content) VALUES (?, ?, ?)",
#            ("4.jpg", "اولین بلاگ مدرسه", "در این پست قابلیت های مختلف سایت را تست میکنیم ."))
#
#cur.execute("INSERT INTO posts (img, title, content) VALUES (?, ?, ?)",
#            ("4.jpg", "نفرات برتر آزمون قلمچی", "نفرات برتر را در عکس زیر مشاهده میکنید."))
#
#cur.execute("INSERT INTO posts (img, title, content) VALUES (?, ?, ?)",
#            ("4.jpg", "علی", "پست 3 برای تست متن اضافه هم ندارم که اضافه کنمممممممم . . . ."))
#
#cur.execute("INSERT INTO posts (img, title, content) VALUES (?, ?, ?)",
#            ("4.jpg", "سارینا", "پست 4 برای تست متن اضافه هم ندارم که اضافه کنمممممممم . . . ."))
#
#cur.execute("INSERT INTO posts (img, title, content) VALUES (?, ?, ?)",
#            (None, "سینا", "پست 5 برای تست متن اضافه هم ندارم که اضافه کنمممممممم . . . ."))
# posts = cur.execute("SELECT * FROM posts")
# for post in posts:
#     cur.execute("DELETE FROM posts WHERE id = ?", (post["id"]))
connection.commit()
connection.close()