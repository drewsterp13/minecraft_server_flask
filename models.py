from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin, LoginManager
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import secrets
import uuid

login_manager = LoginManager()
db = SQLAlchemy()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(25))
    last_name = db.Column(db.String(25))
    email = db.Column(db.String(50), nullable = False)
    password = db.Column(db.String(), default = " ")
    token = db.Column(db.String, default = " ", unique = True)
    g_auth_verify = db.Column(db.Boolean, default = False)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.now)
    
    def __init__(self, first_name, last_name, email, password = " ", token = " ", g_auth_verify = False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = self.set_password(password)
        self.token = self.set_token()
        self.g_auth_verify = self.g_auth_verify

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, your_password):
        self.hash_password = generate_password_hash(your_password)
        return self.hash_password
    
    def set_token(self):
        return secrets.token_hex(12)
    
    def __repr__(self):
        return f"LOG: {self.first_name} {self.last_name} ({self.email}) now has access to this database"
    
class Server(db.Model):
    id = db.Column(db.String(), primary_key = True)
    ip = db.Column(db.String(100))
    port = db.Column(db.Integer)
    hostname = db.Column(db.String(100))
    version = db.Column(db.String(50))
    motd = db.Column(db.String(200))
    max_players = db.Column(db.Integer)
    user_token = db.Column(db.String, db.ForeignKey("user.token"))

    def __init__(self, ip, port, hostname, version, motd, max_players, user_token = " ", id = " "):
        self.id = self.set_id()
        self.ip = ip
        self.port = port
        self.hostname = hostname
        self.version = version
        self.motd = motd
        self.max_players = max_players
        self.user_token = user_token
    
    def set_id(self):
        return (secrets.token_urlsafe())
    
    def __repr__(self):
        return f"LOG: added a server to the database with the ip of {self.ip}"

class ServerSchema(ma.Schema):
    class Meta:
        fields = ["id", "ip", "port", "hostname", "version", "motd", "max_players", "user_token"]

server_schema = ServerSchema()
server_schema_list = ServerSchema(many = True)