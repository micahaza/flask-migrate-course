from flask import Flask, jsonify, json
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
    courses = db.relationship("Course", lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'email_verified': self.email_verified,
            'active': self.active,
            'courses': [c.to_dict() for c in self.courses]
        }


class Course(db.Model, TimeStampMixin):

    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(64), index=True, unique=True)
    active = db.Column(db.Boolean, nullable=False, default=False)
    sections = db.relationship("Section", lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'active': self.active,
            'sections': [s.to_dict() for s in self.sections]
        }


class Section(db.Model, TimeStampMixin):

    __tablename__ = 'sections'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    lectures = db.relationship("Lecture", lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title
        }


class Lecture(db.Model, TimeStampMixin):

    __tablename__ = 'lectures'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id'))
    active = db.Column(db.Boolean, nullable=False, default=False)


@app.route('/', methods=['GET'])
def index():
    return 'Hi everyone, happy coding! Welcome to another episode of get certified.'


@app.route('/seed', methods=['GET'])
def seed():
    user_data = '{"username": "test","first_name": "Test", "last_name": "User","email": "test_user@getcertified.io"}'
    json_data = json.loads(user_data)
    user = User(**json_data)

    course_data = '{"title": "Flask-Migrate Course"}'
    json_data = json.loads(course_data)
    course = Course(**json_data)
    user.courses.append(course)

    section_data = '{"title": "Introduction"}'
    json_data = json.loads(section_data)
    section = Section(**json_data)
    user.courses[0].sections.append(section)

    section_data = '{"title": "What is Flask and Flask-Migrate?"}'
    json_data = json.loads(section_data)
    section = Section(**json_data)
    user.courses[0].sections.append(section)

    db.session.add(user)
    db.session.commit()
    return 'Done'


@app.route('/get_user/', methods=['GET'])
def get_user_data():
    return jsonify(User.query.first().to_dict())


app.run()
