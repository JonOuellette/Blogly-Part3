"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension   
from models import db, connect_db, User, Post, Tag

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'blogly1234'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)
app.app_context().push()

connect_db(app)
db.create_all()


@app.route('/')
def home():
    """shows home page with recent list of posts"""
    
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("posts/homepage.html", posts=posts)


@app.errorhandler(404)
def page_not_found(e):
    """Show 404 error Page Not Found."""

    return render_template('404.html'), 404

@app.route('/users')
def users_list():
    """Shows a page with the list of all users"""
    users = User.query.all()
    return render_template('users/index.html', users=users)


@app.route('/users/new', methods = ["GET"])
def new_user_form():
    """shows a page to create a new user"""

    return render_template('users/new.html')

@app.route('/users/new', methods = ["POST"])
def new_user():
    """handles the submisison to create a new user"""
    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)
    
    db.session.add(new_user)
    db.session.commit()
    flash(f"User {new_user.first_name} {new_user.last_name} added.")

    return redirect("/users")

@app.route("/users/<int:user_id>")
def show_user(user_id):
    """shows information with information on a specific/selected user"""
    user = User.query.get_or_404(user_id)
    return render_template('users/details.html', user=user)

@app.route("/users/<int:user_id>/edit")
def edit_user(user_id):
    """Shows a page to edit the information on an existing user"""
    user= User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def update_user(user_id):
    """Handles the submission to update the information on an existing user"""
    user= User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()
    flash(f"User {new_user.first_name} {new_user.last_name} edited.")

    return redirect("/users")

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Handles submission to delete an existing user"""
    user= User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"User {new_user.first_name} {new_user.last_name} deleted.")

    return redirect('/users')


@app.route('/users/<int:user_id>/posts/new')
def post_form(user_id):
    """Displays a form to submit a post"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('posts/new.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def new_post(user_id):
    """Handles the submission for creating a new post for a specific user"""
    user = User.query.get_or_404(user_id)
    tag_ids =[int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    new_post = Post(title=request.form['title'],content=request.form['content'],user=user, tags=tags)

    db. session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added.")

    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """ Displays a page with info on a user post"""

    post = Post.query.get_or_404(post_id)
    return render_template('posts/show.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """Displays form to edit an existing post"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('posts/edit.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def update_post(post_id):

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' edited.")
    flash(f"Post '{post.title}' edited.")

    return redirect(f"/users/{post.user_id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Handle form submission for deleting an existing post"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title} deleted.")

    return redirect(f"/users/{post.user_id}")

@app.route('/tags')
def tags_index():
    """shoes page with tag info"""
    tags = Tag.query.all()
    return render_template('tags/index.html', tags=tags)

@app.route('/tags/new')
def tags_new_form():
    """Displays form to create a new tag"""
    
    posts = Post.query.all()
    return render_template('tags/new.html', posts=posts)

@app.route("/tags/new", methods=["POST"])
def new_tag():
    """Handles form submission to create a new tag"""

    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()
    flash(f"Tag '{new_tag.name}' added.")

    return redirect("/tags")

@app.route('/tags/<int:tag_id>')
def show_tags(tag_id):
    """Displays a page containing info on a specific tag"""

    tag = Tag.query.get.or_404(tag_id)
    return render_template('tags/show.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit')
def edit_tags_form(tag_id):
    """Displays form to edit tags"""

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('tags/edit.html', tag=tag, posts = posts)    

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def edit_tags(tag_id):
    """Handle form submission for updating an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' edited.")

    return redirect("/tags")   

@app.route('/tags/<int:tag_id>/delete', method=["POST"])
def delete_tags(tag_id):
    """Handles deletion of existing tags"""

    tag=Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' deleted.")

    return redirect("/tags")