from config import db
from datetime import datetime
class Details(db.Model):
    __tablename__ = 'details'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    address = db.Column(db.String(100), nullable=True)
    dob = db.Column(db.DateTime, nullable=False)

    def __init__(self, user_id, address, dob):
        self.user_id = user_id
        self.address = address
        self.dob = datetime.strptime(dob,'%Y-%m-%d')

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'address': self.address,
            'dob':datetime.strftime(self.dob,'%d-%M-%Y')
        }


class Credential(db.Model):
    __tablename__ = 'credential'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    cpassword = db.Column(db.String(300), nullable=True)

    def __init__(self, user_id, password):
        self.user_id = user_id
        self.cpassword = password

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'cpassword': self.cpassword
        }


class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(40), nullable=False)
    Lastname = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    phone = db.Column(db.Integer, unique=True, nullable=False)
    details = db.relationship(
                        'Details',backref='user',uselist=False)
    password = db.relationship(
        'Credential', backref='user', uselist=False)
    roll = db.Column(db.String(4), nullable=False)

    def __init__(self, firstname, lastname, email, phone, address, dob, password, roll):
        self.email = email
        self.roll = roll
        self.firstname = firstname
        self.Lastname = lastname
        self.phone = phone
        self.details = Details(user_id=self.id, address=address, dob=dob)
        self.password = Credential(user_id=self.id, password=password)


    def serialize(self):
        # print(self.details[0].serialize())
        data = {'id': self.id,
                'firstname': self.firstname
                }
        return data

  


# if __name__ == '__main__':
    # db.drop_all()
    # db.create_all()


