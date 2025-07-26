# license_plate_detect

license detection model by trungdinh22
Github repository: https://github.com/trungdinh22/License-Plate-Recognition

## Prerequisites
1. MySQL Server
2. Python 3.11+
3. A Google Map API Key that have accessed to Maps JavaScript API, Geocoding API and Directions API

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/LMysteria/license_plate_detect.git
    cd license_plate_detect
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install the required packages:**
    
    **Install python packages**
    ```bash
    pip install -r requirements.txt
    ```

    **Install React package**
    ```bash
    cd frontend
    npm i
    ```

4. **Install MySQL**

    Skip if you already have MySQL installed

    MySQL official installer guide documentation on: https://dev.mysql.com/doc/mysql-installer/en/

5. **Set database environment keys:**

    Create a file named `db.env` in `App/keys` directory with the following content:

    ***Change the value to match with your MySQL configuration***
    ```
    DBUSERNAME=root
    DBPASSWORD=secret
    DBHOST=localhost
    DATABASE=license_plate
    ```

6. **Set GoogleMap environment key:**

    **Enable Maps JavaScript API, Geocoding API and Directions API on Google Cloud**
    
    Google API Lists: https://console.cloud.google.com/google/maps-apis/api-list

    **Create GoogleAPI Key that have access to Maps JavaScript API, Geocoding API and Directions API**

    Setting up Google API keys guide: https://support.google.com/googleapi/answer/6158862?hl=en

    Create a file named `.env` in `frontend` directory with the following content:

    ***Change the value to match with Google API key***
    ```
    REACT_APP_GOOGLE_MAPS_API_KEY=YOUR_KEY
    ```
    
## Run The Application
**The application need two terminals, one for backend server and one for frontend server**
1. **Start the backend server:**
    
    One terminal at the current working directory (license_plate_detect):

    ```
    fastapi run --workers 3 App/api.py
    ```

2. **Start the frontend server:**
    
    Another terminal at the current working directory (license_plate_detect):

    ```
    cd frontend
    npm start
    ``` 

