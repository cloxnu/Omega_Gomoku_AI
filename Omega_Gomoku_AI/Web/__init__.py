from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'


@app.route('/')
def welcome():
    return render_template('welcome.html')


from Web import web_configure
from Web import web_start

app.register_blueprint(web_configure.bp)
app.register_blueprint(web_start.bp)

web_start.socket_io.init_app(app)
