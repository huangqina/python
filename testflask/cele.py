from flask import Flask
import time
app = Flask(__name__)
@app.route('/')
def hello_world():
    time.sleep(10)
    return 'Hello World!'

@app.route('/index')
def beijing():
    return 'Beijing'
if __name__ == '__main__':
    app.run(threaded = True)