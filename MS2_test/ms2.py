from flask import Flask, render_template
app = Flask(__name__)




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




@app.route('/') # home page of the website
def home():
    return render_template('login.html', title = 'Welcome To Our Page')

@app.route('/main') 
def main():
    return render_template('main.html', posts = posts, title = 'Main')


@app.route('/about')
def hello():
	return  render_template('about.html')


if __name__ == '__main__':
	app.run(debug = True)