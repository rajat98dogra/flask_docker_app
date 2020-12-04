import sys

from webapp.model import User, db
import json

class Database:
    def createdb(self):
        db.drop_all()
        db.create_all()
        print("database create")

    def backup(self,path):
        users=User.query.all()
        data={}
        data['db']=[]
        with open(path+'/db.json', 'w') as f:
            for i in users:
                data['db'].append(i.dbserialize())
                print(i.serialize())
            json.dump(data,f,indent=4)

    def Import(self,file_path):
        with open(file_path, 'r') as f:
            u=eval(f.read())
            # print(u)
            for user in u['db']:
                # print(user)
                obj=User(firstname=user['firstname'],lastname=user['lastname'],
                         email=user['email'],phone=user['phone'],address=user['address'],
                         roll=user['roll'],password=user['password'],dob=user['dob'])
                db.session.add(obj)
                db.session.commit()


