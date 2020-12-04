from config import *
from models import User,Details
from sqlalchemy import or_,and_
import jwt

def task(name,address):
    if address!=' ':
        users = User.query.filter(and_(User.firstname.like(f'{name}%'), Details.address.like(f"{address}"))).all()
    else:
        users = User.query.filter(User.firstname.like(f'{name}%')).all()
    users = list(map(lambda x: x.serialize(), users))
    return jsonify({'users': users})


class Find(Resource):
    def get(self, name, address):
        token = request.args.get('token')
        try:
            jwt.decode(token, 'secretkey')
            return task(name, address)
        except Exception as e:
            print(e)
            return e


api.add_resource(Find,'/<name>/<address>')

if __name__ == '__main__':
    app.run(host='0.0.0.0')