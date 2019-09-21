from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy, event
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://demouser:demopass@localhost/flask_migrate_demo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
migrate = Migrate()
db.init_app(app)
migrate.init_app(app, db)


class TimeStampMixin(object):
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at._creation_order = 9998
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at._creation_order = 9998
    deleted_at = db.Column(db.DateTime)
    deleted_at._creation_order = 9998

    @staticmethod
    def _set_updated_at(mapper, connection, target):
        target.updated_at = datetime.utcnow()

    @classmethod
    def __declare_last__(cls):
        event.listen(cls, 'before_update', cls._set_updated_at)

    def is_deleted(self):
        return self.deleted_at is not None


class User(db.Model, TimeStampMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    first_name = db.Column(db.String(256))
    last_name = db.Column(db.String(256))
    email = db.Column(db.String(120), index=True, unique=True)
    email_verified = db.Column(db.Boolean, nullable=False, default=False)
    password_hash = db.Column(db.String(128))
    active = db.Column(db.Boolean, nullable=False, default=False)


class Course(db.Model, TimeStampMixin):

    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(64), index=True, unique=True)
    active = db.Column(db.Boolean, nullable=False, default=False)


class Section(db.Model, TimeStampMixin):

    __tablename__ = 'sections'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    lecture_id = db.Column(db.Integer, db.ForeignKey('lectures.id'))


class Lecture(db.Model, TimeStampMixin):

    __tablename__ = 'lectures'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    active = db.Column(db.Boolean, nullable=False, default=False)


@app.route('/', methods=['GET'])
def index():
    return 'Hi everyone, happy coding! Welcome to another episode of get certified.'

app.run()
