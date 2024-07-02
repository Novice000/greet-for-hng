from flask import Flask, request, jsonify, redirect
import requests
#rom urllib2 import urlopen

app = Flask(__name__)
api_key = "2654ccb2de5f3685b96fa2c2dc1d2f21"

@app.route("/")
def good():
    return redirect("api/hello?visitor_name=HNG") 
    
@app.route("/api/hello", methods=["GET"])
def food():
    
    #from stackoverflow to help servers with proxy do one or two
    if request.headers.getlist("X-Forwarded-For"):
        IP = request.headers.getlist("X-Forwarded-For")[0]
    else:
        IP = request.remote_addr
        
    visitor_name = request.args.get("visitor_name")
    url = f'http://ip-api.com/json/{IP}'
    response = requests.get(url)
    data = response.json()
    city = data['city']
    country=data['country']
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city
    response = requests.get(complete_url)
    x = response.json()

    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"]
        obj = {
            "client_ip": IP,
            "greeting": f"Hello, {visitor_name}!, the temperature is {int(current_temperature) - 273.5} degrees Celsius in {city}",
            "location": city
        }
        
    return jsonify(obj)

if __name__ == '__main__':
    app.run(debug=True)