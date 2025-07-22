from flask import Flask, render_template, request
from weather import getCurrentWeather
from waitress import serve

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/weather")
def getWeather():
    city = request.args.get("city")

    if not bool(city.strip()):
        city = "Kitchener"

    weather_data = getCurrentWeather(city)

    if not weather_data["cod"] == 200:
        return render_template("city_not_found.html")

    icon_url = getWeatherIcon(weather_data["weather"][0]["icon"])

    return render_template(
        "weather.html",
        title=weather_data["name"],
        country=weather_data["sys"]["country"],
        status=weather_data["weather"][0]["description"].title(),
        temp=f"{weather_data['main']['temp']:.1f}",
        temp_low=f"{weather_data['main']['temp_min']:.1f}",
        temp_high=f"{weather_data['main']['temp_max']:.1f}",
        feels_like=f"{weather_data['main']['feels_like']:.1f}",
        icon_url=icon_url,
    )


def getWeatherIcon(icon_code):

    icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
    return icon_url


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
