
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import  environ



app = Flask(__name__)
name=environ.get('ROOT_USER')
password=environ.get('ROOT_PASSWORD')
host=environ.get('HOST')
database = environ.get('DB_NAME')

config={'user':name,'password':password,'host':host,'database':database}

print(config)

app.config['SQLALCHEMY_DATABASE_URI'] =f'mysql+pymysql://{name}:{password}@{host}/{database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key = '%334!@#$%'

db = SQLAlchemy(app)
db.init_app(app)
from webapp import routes
