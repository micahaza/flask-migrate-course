from flask import Flask

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return 'Hi everyone, happy coding! Welcome to another episode of get certified.'


app.run()
