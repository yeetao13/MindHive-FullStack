import sqlite3
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///outlets.db'
db = SQLAlchemy(app)

class Outlet(db.Model):
    __tablename__ = 'outlets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(255))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

@app.route('/outlets', methods=['GET'])
def get_outlets():
    
    conn = sqlite3.connect('outlets.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM outlets')
    items = cursor.fetchall()
    outlet_list = []
    for item in items:
        id, name, address, lat, long = item
        outlet_data = {
            'id': id,
            'name': name,
            'address': address,
            'latitude': lat,
            'longitude': long
        }
        outlet_list.append(outlet_data)
    conn.close()    
    return jsonify({'outlets': outlet_list})


if __name__ == '__main__': 
    app.run(debug=True)

    
