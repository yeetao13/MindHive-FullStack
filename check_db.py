# checking database items

import sqlite3
conn = sqlite3.connect('outlets.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM outlets')
items = cursor.fetchall()

for item in items:
    id, name, address, lat, long = item
    print(f"ID: {id}, Name: {name}, Address: {address}, Latitude: {lat}, Longitude: {long}")
conn.close()