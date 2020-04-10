import mysql.connector
import hashlib
from flask import Flask, render_template, url_for, flash, redirect
from form import RegistrationForm, LoginForm

#mysql connection
#!!!parameters must be changed according to the server !!!
mydb = mysql.connector.connect(user='root',
                              host='127.0.0.1',
                              password='123',
                              auth_plugin='mysql_native_password',
                              database = 'mydatabase'
                              )

mycursor = mydb.cursor()

app = Flask(__name__)

app.config['SECRET_KEY'] = '226e42e17768b4531ea8bebd49dc1ab7'


@app.route("/")
@app.route("/home")
def home():
    select_stmt = "SELECT username,email,address,dateCreated FROM users"
    mycursor.execute(select_stmt)
    posts = []
    for x in mycursor:
        posts.append({
        'author' : x[0],
        'title'  : x[1],
        'content': x[2],
        'date_posted'   : x[3]
    })
    return render_template('home.html', posts = posts)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        insert_stmt = (
         "INSERT INTO users (username, password, email, address)"
         "VALUES (%s, %s, %s, %s)")
        hashed_password = hashlib.sha256(str(form.password.data).encode('utf-8')).hexdigest()
        data = (form.username.data, hashed_password, form.email.data, form.address.data)
        mycursor.execute(insert_stmt, data)
        mydb.commit()
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        select_stmt = "SELECT username FROM users WHERE email = %(x)s and password = %(y)s"
        hashed_password = hashlib.sha256(str(form.password.data).encode('utf-8')).hexdigest()
        mycursor.execute(select_stmt, { 'x': form.email.data, 'y' : hashed_password})
        flag = False
        for x in mycursor:
            flag = True
            flash(f'Welcome again {x[0]}!', 'success')
        if flag:   
            return redirect(url_for('home'))
        else:
            flash('There is something wrong, I can feel it', 'danger')
    return render_template('login.html', title='Login', form=form)

if __name__ == '__main__':
    app.run(debug=True)