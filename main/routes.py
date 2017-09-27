from main import app
from models import User, db


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/adduser')
def add_user():
    user1 = User('ethan', 'ethan@example.com')
    user3 = User('guest', 'guest@example.com')
    user4 = User('joe', 'joe@example.com')
    user5 = User('michael', 'michael@example.com')

    db.session.add(user1)
    db.session.add(user3)
    db.session.add(user4)
    db.session.add(user5)

    db.session.commit()

    return "<p>add succssfully!"


@app.route('/all')
def all():
    users = User.query.all()
    print users
    return "hello"
