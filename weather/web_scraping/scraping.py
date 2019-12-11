import requests
from bs4 import BeautifulSoup
import datetime

'''
{
"main":{"temp":266.052,
        "temp_min":266.052,
        "temp_max":266.052,
        "pressure":957.86,
        "sea_level":1039.34,
        "grnd_level":957.86,
        "humidity":90},
"wind":{"speed":1.16,
        "deg":139.502},
"clouds":{"all":0},
"weather":[{"id":800,"main":"Clear","description":"Sky is Clear","icon":"01n"}],
"dt":1485722804}
'''

def get_weather(api_key,location,start,end):
    url = "http://history.openweathermap.org/data/2.5/history/city?id={}&type=hour&start={}&end={}&appid={}".format(location,start,end,api_key)
    r = requests.get(url)

    data = r.json()

    dic = {}
    for weather in data["list"]:
        temp = weather["main"]["temp"]-273
        humidity= data["main"]["humidity"]
        wind=data["wind"]["speed"]
        main = weather["weather"]["main"]
        description = weather["weather"]["description"]
        date = datetime.datetime.utcfromtimestamp(weather["dt"])
        dic[date] = [temp,humidity,wind,main,description]

    df = pd.DataFrame.from_dict(dic, orient = "index", columns = ["Temperature","Humidity", "Wind", "Weather", "Description"])
    return df

def request_handler(request):
    if(request['method']=='POST'):
            try:

                city=request['form']['q']
                #length=int(request['values']['len'])
                to_send = "http://api.openweathermap.org/data/2.5/weather?q={}&appid=4630b638d9fb587bae1a92c5671df384".format(city)
                r = requests.get(to_send)
                data = r.json()
                temperature=data["main"]["temp"]-273
                humidity= data["main"]["humidity"]
                wind=data["wind"]["speed"]
                
                
                return "current temperature: "+str(round(temperature))+"C, humidity: "+str(humidity)+"% wind speed: "+str(wind)+" m/s"
            except:
                return '-1'

def main():
    api_key = "4630b638d9fb587bae1a92c5671df384"
    city_id = "4274994"
    ## 2019/01/01/00:00:00 EST = 2019/01/01/05:00:00 UTC
    start = 1546318800
    ## 2019/01/07/23:00:00 EST = 2019/01/08/04:00:00 UTC
    end = 1546920000
    week = 604800

    response = get_weather(api_key,city_id,start,end)
    response.to_csv("")

if __name__ == '__main__':
    main()


