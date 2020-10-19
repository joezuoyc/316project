  
from flask import render_template, url_for, flash, redirect, request
from scheduler import app, db, bcrypt
from scheduler.forms import RegistrationForm, LoginForm, UpdateAccountForm, AnnouncementForm, TaskForm
from scheduler.models import User, Announcement, Task
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
from PIL import Image

# posts = [

# {

# 	'author':'atsushi', 
# 	'title':'blog post 1',
# 	'date': 'Oct 3rd 2020',
# 	'content':'test1'

# },


# {

# 	'author':'hanyca', 
# 	'title':'blog post 2',
# 	'date': 'Oct 3rd 2020',
# 	'content':'test2'

# }

# ]




@app.route('/') # home page of the website, login here
def home():
	return render_template('home.html')
@app.route('/main') # main user page
def main():
	announcements = Announcement.query.all()
	return render_template('main.html', announcements =announcements, title = 'Main')


@app.route('/about')
def about():
	return  render_template('about.html', title = 'About')

@app.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if current_user.is_authenticated:
		return redirect(url_for('main'))
	if form.validate_on_submit():
		hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_pw, logged_hours = form.logged_hours.data, user_identity = form.user_identity.data, status_active = form.status_active.data)
		db.session.add(user)
		db.session.commit()		
		flash(f'Account created for {form.username.data}!', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if current_user.is_authenticated:
		return redirect(url_for('main'))
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		# check if login email and pw is ocrrect
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('main'))
		else:
			flash('Login Unsuccessful. Please check email and password', 'danger')
	return render_template('login.html', title='Login', form=form)





@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))

# save the pic into static/profile_pics
def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splittext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
	# resize the image to (125, 125)
	output_size = (125, 125)
	i = Image.open(picture_path)
	i.thumbnail(output_size)
	i.save(picture_path)
	return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		current_user.username = form.username.data
		current_user.email    = form.email.data
		db.session.commit()
		flash('your account has been update','success')
		return redirect(url_for('account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static', filename = 'profile_pics/' + current_user.image_file)
	return render_template('account.html', title='Account', 
								image_file = image_file, form = form)




@app.route("/announcements/new", methods=['GET', 'POST'])
@login_required
def new_announcement():
	form = AnnouncementForm()
	if form.validate_on_submit():
		announcement = Announcement(title = form.title.data, content = form.content.data, author = current_user)
		db.session.add(announcement)
		db.session.commit()
		flash('Your accoucement has been created', 'success')
		return redirect(url_for('main'))
	return render_template('new_announcement.html', title='New accouncement', form = form)

@app.route("/announcements/<announcement_id>")
def announcement(announcement_id):
	announcement = Announcement.query.get_or_404(announcement_id)
	return render_template('announcement.html', title= announcement.title, announcement = announcement)