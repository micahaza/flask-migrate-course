from flask import Flask

app = Flask(__name__)


class User:
    def __init__(self, name, email_address):
      self.name = name
      self.email_address = email_address


@app.route('/', methods=['GET'])
def index():
    alice = User('Alice', 'alice@getcertified.io')
    bob = User('Bob', 'bob@getcertified.io')

    return 'Hi everyone, happy coding! Welcome to another episode of get certified.'


app.run()
