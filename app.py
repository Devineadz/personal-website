import csv

from flask import Flask, render_template, url_for, request, redirect, session, flash
from flask_bootstrap import Bootstrap

from forms import ContactForm, LoginForm, BlogForm

app = Flask(__name__)
app.secret_key = 'gHoidf293JKL'
Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/CV')
def cv():
    return render_template('CV.html')


@app.route('/Projects')
def projects():
    return render_template('Projects.html')


@app.route('/Blog')
def blog():
    with open(r'data/blog_posts.csv') as csv_file:
        data = csv.reader(csv_file, delimiter=',')
        posts = []
        for row in data:
            if row:
                posts.append({
                    "topic": row[0],
                    "matter": row[1],
                    "subject": row[2]
                })
    return render_template('Blog.html', posts=posts)


@app.route('/Contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        with open('data/contact.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([form.name.data, form.email.data, form.message.data])
        return redirect(url_for('contact_success'))
    return render_template('Contact.html', form=form)


@app.route('/Contact_success')
def contact_success():
    return render_template('Contact_success.html')


@app.route('/Login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        #Dummy username = test_admin and pw test123
        if request.form['username'] == 'test_admin' and request.form['password'] == 'test123':
            session['username'] = form.username.data
            return redirect(url_for('admin'))
        else:
            flash('Either username or password not correct. Please enter again')
    return render_template('Login.html', form=form)


@app.route('/Admin')
def admin():
    #Check if user logged in to give access to page, otherwise direct to login
    if 'username' in session:
        username = session['username']
        with open(r'data/contact.csv') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            contacts = []
            for row in reader:
                if row:
                    contacts.append({"sender": row[0], "email": row[1]})
        return render_template('Admin.html', username=username, contacts=contacts)
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))


@app.route('/Post_blog', methods=['GET', 'POST'])
def post_blog():
    # Check if user logged in to give access to page, otherwise direct to login
    form2 = BlogForm()
    if 'username' in session:
        if form2.validate_on_submit():
            with open('data/blog_posts.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow([form2.blog_title.data, form2.content.data, form2.topic_area.data])
            return redirect(url_for('successful_post'))
        return render_template('Post_blog.html', form2=form2)
    else:
        flash('Log in first!')
        return redirect(url_for('login'))


@app.route('/Successful_post')
def successful_post():
    return render_template('Successful_post.html')


if __name__ == '__main__':
    app.run()
