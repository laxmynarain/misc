import urllib, json
from math import radians, cos, sin, asin, sqrt
from datetime import timedelta, datetime
import time

URL = "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson"
EARTH_RADIUS_MILES = 3959
INTERANA_LONG_LAT = [-122.166213, 37.452234]


class quake():
    def __init__(self, magnitude=0, longitude=0, latitude=0, place='', event_time=0, distance=0):
        self.magnitude = magnitude
        self.longitude = longitude
        self.latitude = latitude
        self.place = place
        self.event_time = event_time
        self.distance = distance

def gethighestmagnitude(url=URL):
    q = quake()
    quakelist=[]
    features = getdata(url)['features']
    for data in features:
        ep_time = data['properties']['time']
        if lessthanaweek(ep_time):
            curr_location =  data['geometry']['coordinates']
            distance = haversine_distance(curr_location)
            if distance <= 100:
                curr_magnitude = data['properties']['mag']
                if curr_magnitude == q.magnitude:
                    q = quake(curr_magnitude, curr_location[0], curr_location[1], data['properties']['place'], ep_time, distance)
                    quakelist.append(q)
                elif curr_magnitude > q.magnitude:
                    quakelist = []
                    q = quake(curr_magnitude, curr_location[0], curr_location[1], data['properties']['place'], ep_time, distance)
                    quakelist.append(q)

    return quakelist


def getdata(url):
    response = urllib.urlopen(url);
    return json.loads(response.read())


def lessthanaweek(ep_time):
    seven_day_epoch = time.mktime((datetime.now() - timedelta(days=7)).timetuple())*1000
    if ep_time > seven_day_epoch:
        return True
    else:
        return False


def haversine_distance(loc, ref_loc = INTERANA_LONG_LAT):
    lon1, lat1 = loc[:2]
    lon2, lat2 = ref_loc
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine_distance formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    distance = EARTH_RADIUS_MILES * c
    return distance


if __name__ == '__main__':
    quakeslist = gethighestmagnitude()
    if quakeslist:
        for quake in quakeslist:
            print 'A Quake of Magnitude {0} occured on {1} ({2}) at longitude {3} ' \
                  'and latitude {4}. A distance of {5} miles from Interana'.format(quake.magnitude, time.ctime(quake.event_time/1000), quake.place, quake.longitude, quake.latitude, quake.distance)
    else:
        print 'No Quake found within 100 mile radius of Interana in the last 7 days'

