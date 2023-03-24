from flask import Flask

app = Flask(__name__)

# Route the index page
@app.route('/')
def index():
    return 'Hello all!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)