from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
# from flask_app_template.models.user import user 

@app.route('/')
def log_and_reg():
    return render_template('log_and_reg.html')

@app.route('/login', methods=['POST'])
def login():
    #validate login form
    if not User.validate_login(request.form):
        return redirect('/')
    user = User.get_user_by_email(request.form)
    if user:
        # if user exists, check if password matches
        if not bcrypt.check_password_hash(user.password, request.form['password']):
            # if password did not match
            flash('Email/Password combination is incorrect')
            return redirect('/')

        # if password matched
        session['user_id'] = user.id
        flash('Login was successful!')
        return redirect('/dashboard')
        
    flash('Email is not tied to an account')
    return redirect('/')
        # return user to form with validations
        

@app.route('/register', methods=['POST'])
def register():
    #validate register form
    if not User.validate_register(request.form):
        return redirect('/')
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    register_data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash
    }

    user_id = User.register_user(register_data)
    session["user_id"] = user_id
    flash('Registration was succesful!')
    return redirect('dashboard')


@app.route('/dashboard')
def user_dashboard():
    user_data = {
        'id': session['user_id']
    }
    user = User.get_user_by_id(user_data)
    return render_template('dashboard.html', user=user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')