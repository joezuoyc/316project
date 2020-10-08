  
from flask import render_template, url_for, flash, redirect
from scheduler import app
from scheduler.forms import RegistrationForm, LoginForm
from scheduler.models import User, Announcement



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




@app.route('/', methods = ['GET', 'POST']) # home page of the website, login here
def home():
	return render_template('home.html', posts=posts)


@app.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		flash(f'Account created for {form.username.data}!', 'success')
		return redirect(url_for('home'))
	return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'test@test.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('main'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/main') # main user page
def main():
	return render_template('main.html', posts = posts, title = 'Main')


@app.route('/about')
def about():
	return  render_template('about.html')


if __name__ == '__main__':
	app.run(debug = True)