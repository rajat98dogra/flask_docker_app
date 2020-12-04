from webapp.routes import *

def adminUpdate(user ,id):

    form = AdminUpdateform()
    if not form.validate_on_submit():
        err = list(form.errors.keys())
        if err:
            flash(f'{err[0]} {form.errors[err[0]][0].lower()}', 'danger')
        return redirect(url_for('details', id=id))
    try:
        user.firstname = request.form['firstname']
        user.Lastname = request.form['lastname']
        user.roll = request.form['roll']
        return user
    except:
        flash('Error in Updating', 'danger')
        return redirect(url_for('admin'))


def userUpdate(user ,id):
    form = UserUpdateform()
    # print(request.form['dob'])
    if not form.validate_on_submit():
        err = list(form.errors.keys())
        if err:
            flash(f'{err[0]} {form.errors[err[0]][0].lower()}', 'danger')
        return redirect(url_for('details', id=id))

    olduser = User.query.filter_by(phone=request.form['phone'] and id != id).first()
    if olduser:
        flash('Phone number already Exists', 'danger')
        return redirect(url_for('details', id=id))
    try:
        user.firstname = request.form['firstname']
        user.Lastname = request.form['lastname']
        user.details.address = request.form['address']
        user.phone = request.form['phone']
        user.details.dob = request.form['dob']
        user.email = request.form['email']
        # print(detail.serialize())
        return user
    except:
        flash('Error in Updating', 'danger')
        return redirect(url_for('details', id=id))
