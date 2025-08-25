from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'

db = SQLAlchemy(app)

class URLMap(db.Model):

    __tablename__ = 'urls'

    id = db.Column(db.Integer, primary_key = True)
    long_url = db.Column(db.String(2048), nullable = False)
    short_code = db.Column(db.String(6), unique = True, nullable = False, index = True)
    created_at = db.Column(db.DateTime, nullable = False, default = datetime.timezone.utc)
    # get the itc, indian time - Asia/Kolkata
    # created_at = db.Column(db.DateTime, nullable = False, default = datetime.n) 
    clicks = db.Column(db.Integer, nullable = False, default = 0)

    def __repr__(self):
        return f'<URLMap {self.short_code} -> {self.long_url[:30]}'

@app.route('/')
def hello_world():
    return "Hello, World!"

@app.route('/about')
def about():
    return "About Page"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
    app.run(debug=True)