import requests
url = "https://api.weatherapi.com/v1/current.json?key=YOUR_KEY&q=Dhaka&aqi=yes"
response = requests.get(url)
print(response.json())
