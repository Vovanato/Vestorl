from flask import Flask,request
from werkzeug.security import generate_password_hash
from app.database import get_db_connection
from app.routes.api import vbp
from app.routes.pages import pages_bp
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

app.register_blueprint(vbp)
app.register_blueprint(pages_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)  