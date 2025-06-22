import pytest
import bcrypt
from app import create_app, db
from app.models import UserCredentials, ClientMetadata, ClientSftpMetadata

@pytest.fixture
def test_client():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    })

    with app.test_client() as client:
        with app.app_context():
            db.create_all()

            hashed_password = bcrypt.hashpw("testpass".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            user = UserCredentials(username='testuser', password=hashed_password, role='admin')

            client_metadata = ClientMetadata(client_name='client1', email='client1@example.com')
            db.session.add(client_metadata)
            db.session.flush()  # To get client_metadata.client_id before using it

            sftp = ClientSftpMetadata(
                client_id=client_metadata.client_id,
                sftp_directory='client1',
                sftp_username='sftp_user1',
                password='client1_abcd'
            )

            db.session.add_all([user, sftp])
            db.session.commit()

        yield client

        with app.app_context():
            db.session.remove()
            db.drop_all()
            db.engine.dispose()
