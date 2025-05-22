from flask import Flask, jsonify
import requests
import socket
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration - IMPORTANT: Store your key in .env file!
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY") or "0455e18df57149948c7103130252105"  # TEMPORARY - Remove hardcoded key after testing
LOCATION = "Dhaka,Bangladesh"  # Comma separated, no spaces
VERSION = "v1.0.0"
WEATHER_API_URL = f"https://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={LOCATION}&aqi=yes"

def get_weather():
    """Fetch weather data with proper error handling"""
    try:
        print(f"Attempting to fetch from: {WEATHER_API_URL}")
        response = requests.get(WEATHER_API_URL, timeout=10)
        response.raise_for_status()  # Raises HTTPError for bad responses
        
        data = response.json()
        print("API Response:", data)  # Debug output
        
        return {
            "temperature": data["current"]["temp_c"],
            "temp_unit": "c"
        }
    except requests.exceptions.RequestException as e:
        print(f"Weather API request failed: {str(e)}")
        return None
    except KeyError as e:
        print(f"Unexpected API response format: {str(e)}")
        return None

@app.route("/api/hello", methods=["GET"])
def hello():
    weather = get_weather()
    
    return jsonify({
        "hostname": socket.gethostname(),
        "datetime": datetime.utcnow().strftime("%y%m%d%H%M"),
        "version": VERSION,
        "weather": {
            "dhaka": {
                "temperature": weather["temperature"] if weather else "unavailable",
                "temp_unit": "c"
            }
        }
    })

@app.route("/api/health", methods=["GET"])
def health_check():
    try:
        test = requests.get(WEATHER_API_URL, timeout=5)
        test.raise_for_status()
        return jsonify({
            "status": "healthy",
            "weather_api": "reachable"
        })
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "weather_api": "error",
            "error": str(e)
        }), 503

if __name__ == "__main__":
    # Verify configuration
    if not WEATHER_API_KEY:
        print("Error: WEATHER_API_KEY not set!")
    
    app.run(host="0.0.0.0", port=5000, debug=True)


