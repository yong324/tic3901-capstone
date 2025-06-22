from app import db

class UserCredentials(db.Model):
    __tablename__ = 'user_credentials'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='user')
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())

class ClientMetadata(db.Model):
    __tablename__ = 'client_metadata'
    client_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_name = db.Column(db.String(150), nullable=False, unique=True)
    added_datetime = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    email = db.Column(db.String(255), nullable=False)
    sftp_records = db.relationship('ClientSftpMetadata', backref='client', cascade="all, delete")

class ClientPermissions(db.Model):
    __tablename__ = 'client_permissions'
    client_id = db.Column(db.Integer, db.ForeignKey('client_metadata.client_id'), primary_key=True)
    permission = db.Column(db.String(100), primary_key=True)

class ClientSftpMetadata(db.Model):
    __tablename__ = 'client_sftp_metadata'
    client_id = db.Column(db.Integer, db.ForeignKey('client_metadata.client_id'), primary_key=True)
    sftp_directory = db.Column(db.String(150), nullable=False)
    sftp_username = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(255), nullable=False)
