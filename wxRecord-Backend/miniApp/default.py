from flask import Flask,render_template
from gevent import pywsgi

app = Flask(__name__)
 
@app.route('/')
def index():
    return render_template('')
 
if __name__ == '__main__':
    server = pywsgi.WSGIServer(('0.0.0.0', 80), app)
    server.serve_forever()
    app.run()