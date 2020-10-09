  
from flask import render_template, url_for, flash, redirect, request
from scheduler import app, db, bcrypt
from scheduler.forms import RegistrationForm, LoginForm
from scheduler.models import User, Announcement
from flask_login import login_user, current_user, logout_user, login_required


posts = [

{

	'author':'atsushi', 
	'title':'blog post 1',
	'date': 'Oct 3rd 2020',
	'content':'test1'

},


{

	'author':'hanyca', 
	'title':'blog post 2',
	'date': 'Oct 3rd 2020',
	'content':'test2'

}

]




@app.route('/') # home page of the website, login here
def home():
	return render_template('home.html', posts=posts)
@app.route('/main') # main user page
def main():
	return render_template('main.html', posts = posts, title = 'Main')


@app.route('/about')
def about():
	return  render_template('about.html', title = 'About')

@app.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	# if current_user.is_authenticated:
	# 	return redirect(url_for('main'))
	if form.validate_on_submit():
		hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
		db.session.add(user)
		db.session.commit()		
		flash(f'Account created for {form.username.data}!', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	# if current_user.is_authenticated:
	# 	return redirect(url_for('main'))
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		# check if login email and pw is ocrrect
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash('Login Unsuccessful. Please check email and password', 'danger')
	return render_template('login.html', title='Login', form=form)





@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
	return render_template('account.html', title='Account')