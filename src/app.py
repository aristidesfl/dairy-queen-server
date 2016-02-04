import sys
sys.path.append('./dairy_queen')
import double_dip
import flask

app = flask.Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
