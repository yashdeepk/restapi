from flask_basicauth import BasicAuth

from dbhelper import dbhelper
from user import user

#app.config['BASIC_AUTH_FORCE'] = True

class Auth(BasicAuth):

    def __init__(self, app=None):
        self.app = app
        self.username = ""
        self.dbPath = "proj.db"
        super().__init__(app)

    #override parent function
    def check_credentials(self, username, password):
        obj = user()

        obj.username = username
        obj.password = password

        query = dbhelper.getExistQuery(obj, ["username", "password"])
        conn = dbhelper.initDb(self.dbPath)
        doesExist = dbhelper.executeIfExist(conn, query)
        dbhelper.closeDb(conn)

        if doesExist:
            self.username = obj.username
            self.app.config['BASIC_AUTH_USERNAME'] = username
            return True
        else:
            return False
