"""Blogly application."""

from flask import Flask, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "secret"

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def root():
    return redirect("/users")

@app.route("/users")
def list_users():
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template("users/index.html", users=users)

@app.route("/users/new", methods=["GET"])
def show_new_user_form():
    return render_template("users/new.html")

@app.route("/users/new", methods=["POST"])
def add_new_user():
    from flask import request
    first = request.form["first_name"]
    last = request.form["last_name"]
    img = request.form["image_url"] or None
    user = User(first_name=first, last_name=last, image_url=img or User.image_url.default.arg)
    db.session.add(user)
    db.session.commit()
    return redirect("/users")

@app.route("/users/<int:user_id>")
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("users/show.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["GET"])
def show_edit_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("users/edit.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def update_user(user_id):
    from flask import request
    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]
    db.session.commit()
    return redirect("/users")

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")

# Show new post form
@app.route("/users/<int:user_id>/posts/new")
def new_post_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("posts/new.html", user=user)

# Handle new post submission
@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def handle_new_post(user_id):
    user = User.query.get_or_404(user_id)
    title = request.form["title"]
    content = request.form["content"]
    post = Post(title=title, content=content, user=user)

    db.session.add(post)
    db.session.commit()
    return redirect(url_for('show_user', user_id=user.id))

# Show post detail
@app.route("/posts/<int:post_id>")
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("posts/show.html", post=post)

# Show edit form
@app.route("/posts/<int:post_id>/edit")
def edit_post_form(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("posts/edit.html", post=post)

# Handle post update
@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def handle_edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]
    db.session.commit()
    return redirect(url_for('show_post', post_id=post.id))

# Handle post delete
@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    user_id = post.user.id
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('show_user', user_id=user_id))

# List tags
@app.route('/tags')
def list_tags():
    tags = Tag.query.all()
    return render_template('tags/index.html', tags=tags)

# Show tag detail
@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/show.html', tag=tag)

# New tag form
@app.route('/tags/new')
def new_tag_form():
    return render_template('tags/new.html')

# Handle new tag
@app.route('/tags/new', methods=["POST"])
def create_tag():
    name = request.form['name']
    tag = Tag(name=name)
    db.session.add(tag)
    db.session.commit()
    return redirect('/tags')

# Edit tag form
@app.route('/tags/<int:tag_id>/edit')
def edit_tag_form(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/edit.html', tag=tag)

# Handle tag edit
@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def update_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    db.session.commit()
    return redirect('/tags')

# Delete tag
@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect('/tags')
