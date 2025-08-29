from flask import Flask, request, jsonify
from flask import redirect, abort, render_template
from flask_sqlalchemy import SQLAlchemy
import datetime
from utilis import generate_short_code

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


@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()

    long_url = data.get['long_url'] 
    # with () it will return a default value of None if no value is found, but for [] it will raise a `KeyError`

    if not long_url:
        return jsonify({'error' : 'The "long_url" field is required'}), 400
    
    custom_alias = data.get('custom_alias')

    if custom_alias:
        if ' ' in custom_alias:
            return jsonify({'error' : 'Custom alias contains spaces.'}), 400
        if not custom_alias.isalnum():
            return jsonify({'error' : 'Custom alias can only contains numbers and alphabets'}), 400
        if not (4 <= len(custom_alias) <= 30):
            return jsonify({'error' : 'Custom alias must only be between 4 and 30 character length'}), 400


    short_code = generate_short_code()

    while URLMap.query.filter_by(short_code=short_code).first():
        short_code = generate_short_code()

    new_url_mapping = URLMap(long_url=long_url, short_code=short_code)
    db.session.add(new_url_mapping)
    db.session.commit()

    short_url = f'{request.host_url}{short_code}'

    return jsonify({
        'message' : 'URL shortened successfully.',
        'short_url' : short_url,
        'long_url' : long_url
    }), 201

@app.route('/<string:short_code>')
def redirect_to_long_url(short_code):
    url_map_entry = URLMap.query.filter_by(short_code = short_code).first()

    if url_map_entry:
        url_map_entry.clicks += 1
        db.session.commit()
        long_url = url_map_entry.long_url
        return redirect(long_url)
    else:
        abort(404)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analytics/<string:short_code>')
def show_analytics(short_code):
    url_map_entry = URLMap.query.filter_by(short_code = short_code).first()

    if url_map_entry:
        return render_template('analytics.html', url_data = url_map_entry)
    else:
        abort(404)

@app.route('/about')
def about():
    return "About Page"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)