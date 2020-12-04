
from webapp import *
from webapp.model import User
from flask import render_template, \
    redirect, url_for, request, session, abort, flash,jsonify
from .passwordgen import encode, decode
from .forms import UserUpdateform, AdminUpdateform, RegisterationForm, \
    Loginform
import requests
import json
from webapp.update import adminUpdate , userUpdate
from  functools import  wraps
import jwt
from datetime import datetime ,timedelta

def mylogin_required(func):
    @wraps(func)
    def inner(*args,**kwargs):
        if session.get('id'):
            return  func(*args,**kwargs)
        else:
            return redirect(url_for('myLogin'))
    return inner

def permission(func):
    @wraps(func)
    def inner(*args,**kwargs):
        if session.get('roll')=='A':
            return func(*args,**kwargs)
        else:
            return redirect(url_for('home'))
    return inner

@app.route('/home')
@mylogin_required
def home():
    user = User.query.filter_by(id=session['id']).first()
    data = {'user': user.serialize()}
    return render_template('home.html', data=data)



@app.route('/', methods=['GET', 'POST'])
def myLogin():
    form = Loginform()
    if session.get('id'):
        flash('user are already logged In', 'success')
        return redirect(url_for('home'))

    if request.method == 'POST' and form.validate_on_submit():
        email = request.form['email']
        password = request.form['password']
        try:
            user = User.query.filter_by(email=email).first()
        except:
            user = None
        if user:
            if decode(user.password.cpassword, password):
                session['id'] = user.id
                session['roll'] = user.roll
                session['user'] = user.serialize()
             
                return redirect(url_for('home'))
            else:
                flash('Wrong password', 'success')
        else:
            flash('User not Exists', 'danger')
    err = list(form.errors.keys())
    if err:
        flash(f'{err[0]} {form.errors[err[0]][0].lower()}', 'danger')
    return render_template('form.html', form=form)


@app.route('/logout')
@mylogin_required
def myLogout():
    session.clear()
    print(session)
    flash('Log out', 'success')
    return redirect(url_for('myLogin'))


@app.route('/signin', methods=['GET', 'POST'])
def mySign():
    form = RegisterationForm()
    if request.method == 'POST' and form.validate_on_submit():
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        phone = request.form['phone']
        address = request.form['address']
        dob = request.form['dob']
        email = request.form['email']
        password = request.form['password']
        cpassword = request.form['confirmpassword']

        try:
            user = User.query.filter_by(phone=phone).first()
        except:
            user = None
        if not user:
            if password != cpassword:
                flash('confirm password should be same', 'danger')
                return render_template('signin.html')
            else:
                roll = 'U'
                new = User(firstname=firstname, lastname=lastname,
                           email=email, address=address, dob=dob,
                           phone=phone, password=encode(password), roll=roll)
                # print(new)
                db.session.add(new)
                db.session.commit()
                print('created')
                flash('user created successfully', 'success')
                return redirect(url_for('mySign'))
        else:
            flash('Phone no. already exsits', 'danger')
            return redirect(url_for('mySign'))
    err = list(form.errors.keys())
    if err:
        flash(f'{err[0]} {form.errors[err[0]][0].lower()}', 'danger')
    return render_template('signin.html', form=form)


@app.route('/details/<int:id>')
@mylogin_required
def details(id):
    form = UserUpdateform()
    if session['roll'] == 'U' and session['id'] != id:
        return redirect(url_for('home'))
    try:
        user = User.query.filter_by(id=id).first()
    except:
        user = None
    if user:
        data = {'current': session['user'], "user": [user.serialize()]}
        return render_template('details.html', form=form, roll=session['roll'], data=data)
    return abort(status=404)


@app.route('/admin')
@permission
@mylogin_required
def admin():
    if not session.get('id') or session['roll'] != 'A':
        return redirect(url_for('home'))
    try:
        users = User.query.filter(User.id != session['id']).all()
    except:
        return render_template('admin.html', message='No user')
    mess = f'Total Number of user {len(users)}'
    data = {"users": users, 'message': mess, 'value': ''}
    return render_template('admin.html', data=data)


@app.route('/delete/<int:id>')
@permission
@mylogin_required
def myDelete(id):
    try:
        user = User.query.filter_by(id=id).first()
        print(user)
        db.session.delete(user)
        db.session.commit()
        flash('Delete', 'success')
        return redirect(url_for('admin'))
    except:
        flash('Not Delete', 'danger')
        return redirect(url_for('admin'))


@app.route('/update/<int:id>', methods=["POST"])
@mylogin_required
def myUpdate(id):
    try:
        user = User.query.filter_by(id=id).first()
        if session.get('id')!=id:
            user = adminUpdate(user,id)
        else:
            user = userUpdate(user,id)
        try:
            db.session.add(user)
            print(db.session.commit())
            flash('Update', 'success')
            if session['id'] == id:
                return redirect(url_for('details', id=id))
            else:
                return redirect(url_for('admin'))
        except Exception as e:
            flash(f'database error {e}','danger')
            return redirect(url_for('details',id=id))
    except Exception as e:
        flash('Not Updated', 'danger')
        return redirect(url_for('details', id=id))



@app.route('/search', methods=['GET', 'POST'])
@permission
@mylogin_required
def mysearch():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        token = jwt.encode(
            {'user': session['id'],
             'exp': datetime.utcnow() + timedelta(minutes=5)
             }, 'secretkey')

        if name and name!=' ':
            api_url = environ.get('API')
            data= requests.get(f"http://{api_url}/{name}/{address}",{'token':token})
            data=(json.loads(data.text))
            return render_template('admin.html',data=data)

    return redirect(url_for('admin'))
