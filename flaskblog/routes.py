import os 
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog.models import User, Post
from flask_login import login_user, logout_user, current_user, login_required



@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') # use decode because form sending data as string
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account now has been created! You are now able to login ', 'success') # success as categoty to render message in template see in layout.html
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if user and bcrypt.check_password_hash(user.password, form.password.data): # check password is equal or not bcrypt.check_password_hash(user.password(from db), form.password.data(from input form))
                login_user(user, remember=form.remember.data)
                flash('Login Successful!', 'success')
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home')) # [on_true] if [expression] else [on_false] 
            else:
                flash('Password Wrong!', 'danger')
        else:
            flash('Login Unseccessful!, Please check email and password', 'danger') # danger as categoty to render message in template as danger alert
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash('Logout Successful!', 'success')
    return redirect(url_for('home'))


# this function can be rename the filename to hex, resize image size and then save the image into 'static\images\profiles'
def save_image(form_image):
    # generate token_hex and update the image filename
    random_hex = secrets.token_hex(8)
    f_name, f_text = os.path.splitext(form_image.filename)
    image_name = random_hex + f_text
    # direct image to specific path
    image_path = os.path.join(app.root_path, 'static/images/profiles/', image_name)
    print(image_path)
    # resize image
    output_size = (125, 125)
    image = Image.open(form_image)
    image.thumbnail(output_size)
    # save the image
    image.save(image_path)
    return image_name


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm() 
    if form.validate_on_submit():
        if form.image.data:
            form_image = save_image(form.image.data)
            current_user.image = form_image
        current_user.username = form.username.data 
        current_user.email = form.email.data
        db.session.commit()
        flash('Your Account has been Updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    #check the image user
    path_image = app.root_path + '/static/images/profiles/' + current_user.image
    print(path_image)
    is_exist = os.path.exists(path_image)
    if is_exist:
        profile_image = url_for('static', filename='images/profiles/' + current_user.image)
    else:
        profile_image = url_for('static', filename='images/profiles/default.jpg')
    return render_template('account.html', title='Account', profile_image=profile_image, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required 
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Success created Post!', 'success')
        return redirect(url_for('home'))
    return render_template('article/create_post.html', title='Create Article', form=form)


@app.route('/post/<slug>')
def post(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    print(post.slug)
    return render_template('article/post.html', title=post.title, post=post)