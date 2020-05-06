import requests as req
from bs4 import BeautifulSoup
from flask import Flask, render_template

app = Flask(__name__)

def get_info():
    url = 'http://api.irishrail.ie/realtime/realtime.asmx/getStationDataByCodeXML?StationCode=cnlly'
    data = req.get(url)
    soup = BeautifulSoup(data.text, 'xml')

    train_code = soup.find_all('Traincode')
    origin = soup.find_all('Origin')
    destination = soup.find_all('Destination')
    origin_time = soup.find_all('Origintime')
    destination_time = soup.find_all('Destinationtime')
    due_in = soup.find_all('Duein')
    last_location = soup.find_all('Lastlocation')
    last_refreshed = soup.find('Querytime')

    info = []
    for i in range(0, len(train_code)):
        temp = dict(code=train_code[i].text, origin=origin[i].text, destination=destination[i].text,
                    departure= origin_time[i].text, arrival=destination_time[i].text, lastloc=last_location[i].text,
                    due=due_in[i].text)
        info.append(temp)

    return info, last_refreshed.text

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    info, last_refreshed = get_info()
    return render_template('index.html', info=info, last_refreshed=last_refreshed)

if __name__ == '__main__':
    app.run(port=5000, debug=True)