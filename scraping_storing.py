import requests
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
import sqlite3

# Function to handle pagination and scrape all pages
def scrape_all_pages(base_url):
    all_outlets = []
    page = 1
    while True:
        url = f"{base_url}/page/{page}"
        outlets = scrape_page(url)
        
        if not outlets:
            break
        
        all_outlets.extend(outlets)
        page += 1

    return all_outlets


def scrape_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    name_list=[]
    address_list=[]
    outlets =[]
    outlets_list = soup.find_all('div', class_='elementor-element elementor-element-684eb1d elementor-posts--thumbnail-top elementor-grid-3 elementor-grid-tablet-2 elementor-grid-mobile-1 elementor-widget elementor-widget-archive-posts')
    for element in outlets_list:
        # Find all <p> and <a> elements within each element
        names = element.find_all('p',class_="elementor-heading-title elementor-size-default")
        addresses = element.find_all('a',class_="premium-button premium-button-none premium-btn-lg premium-button-none")

        # Process the <p> elements found
        for name in names:
            name_list.append(name.text)
        # Process the <a> elements found
        for address in addresses:
            address_list.append(address.get("href"))
    for i in tuple(zip(name_list,address_list)):
        outlets.append(i)
    
    return outlets

def create_db(all_outlets):
    # Create SQLite database and table
    conn = sqlite3.connect('outlets.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS outlets (
            id INTEGER PRIMARY KEY,
            name TEXT,
            address TEXT
        )
    ''')
    # Insert scraped data into the database
    cursor.executemany('INSERT INTO outlets (name, address) VALUES (?, ?)', all_outlets)
    conn.commit()

    conn.close()

def create_lat_long():
    # Establish connection to the database
    conn = sqlite3.connect('outlets.db')
    cursor = conn.cursor()

    # Retrieve outlets data including addresses
    cursor.execute('SELECT id, name, address FROM outlets')
    outlets_data = cursor.fetchall()
    column_names = [col[1] for col in outlets_data]

    if 'latitude' not in column_names:
        cursor.execute('ALTER TABLE outlets ADD COLUMN latitude REAL')
    if 'longitude' not in column_names:
        cursor.execute('ALTER TABLE outlets ADD COLUMN longitude REAL')


    # Create a geocoder instance for OpenStreetMap Nominatim
    geolocator = Nominatim(user_agent="outlets_geocoder")

    # Update each outlet with its geographical coordinates
    for outlet_id, name, address in outlets_data:
        names = name + ", Melaka" + ", Malaysia"
        print(names)
        print(address)
        location = geolocator.geocode(names)
        if location:
            latitude = location.latitude
            longitude = location.longitude
            cursor.execute('UPDATE outlets SET latitude=?, longitude=? WHERE id=?', (latitude, longitude, outlet_id))
            conn.commit()
        else:
            cursor.execute('UPDATE outlets SET latitude=?, longitude=? WHERE id=?', (-999.0, -999.0, outlet_id))
            conn.commit()

    conn.close()

url = "https://zuscoffee.com/category/store/melaka"       
all_outlets = scrape_all_pages(url)

create_db(all_outlets)
create_lat_long()