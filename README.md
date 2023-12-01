# MindHive-FullStack
This project is a Flask-based web application designed to visualize outlet locations on an interactive map. It offers a user-friendly interface to display outlets and their 5KM radius catchment areas using Leaflet, a JavaScript library for interactive maps.

## Getting Started

To use this application, follow these steps:

### Prerequisites

- Python (3.x recommended)
- Flask
- Flask-SQLAlchemy
- Flask-CORS (for development)

### Installation

1. Clone or download this repository to your local machine.

2. Install the required Python packages using pip:

    ```bash
    pip install BeautifulSoup4
    pip install Flask Flask-SQLAlchemy Flask-CORS
    pip install geopy
    ```

### Usage

1. Run the Flask server:
    
    ```bash
    # Run scraping_storing.py first (outlets.db will be created), then run python app.py.
    python scraping_storing.py
    python app.py
    ```

2. Open the HTML file (`index.html`) in a web browser.

3. View the map:

    - The map will display markers for outlet locations fetched from the Flask API endpoint (`http://127.0.0.1:5000/outlets`).
    - Each outlet will have a 5KM radius catchment area drawn around it.
  
4. Once `outlets.db` database created, no need to run `scraping_storing.py` again.
5. With `check_db.py`, you can check what items are stored in the database (Make sure you have database before running `check_db.py`).

### Troubleshooting

- If encountering CORS issues, ensure that the Flask server has CORS enabled (for development purposes).
- When a web application running in a browser makes a request to a server with a different origin (i.e., domain, protocol, or port), the browser's security policy might block the request due to CORS restrictions. This security mechanism prevents certain types of cross-origin requests to protect users' data and security.
- It allows the frontend (e.g., HTML/JavaScript) hosted on a different port or domain to make requests to the Flask backend API without being blocked by the browser.
- Make sure to specify the right SQLite name (or path) in `app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///outlets.db'` in `scraping_storing.py`. 
- Make sure to specify the right URL to your API endpoint in `index.html` under fetchOutlets() function.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## License

This project is licensed under the [MIT License](LICENSE).
