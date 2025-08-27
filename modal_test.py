import modal
from modal import App, Image

app = modal.App("hello-app")
image = Image.debian_slim().pip_install("requests")

# Hello function
@app.function(image=image, region="eu")
def hello() -> str:
    import requests
    
    response = requests.get('https://ipinfo.io/json')
    data = response.json()
    city, region, country = data['city'], data['region'], data['country']
    return f"Hello from {city}, {region}, {country}!"
