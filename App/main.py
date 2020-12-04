import sys
from webapp import app
from webapp.create_db import Database

if __name__ == '__main__':
    try:
        if sys.argv[1]=='create':
            obj = Database()
            obj.createdb()
            obj.Import(file_path='./db.json')
        elif sys.argv[1]=='run':
            app.run(debug=True,host='0.0.0.0')
        elif sys.argv[1]=='backup':
            obj = Database()
            obj.backup(path='.')
    except:
        app.run(host='0.0.0.0')

