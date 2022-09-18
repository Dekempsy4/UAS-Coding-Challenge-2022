# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

'''
    UAS Coding Challenge
    Back-end Challenge # 2, GPS Speed Challenge
    Author: Felix Toft
'''
from threading import Thread
import http.server, socketserver
import requests, utm, time, math

def main():
    'Starts the server on a seperate thread so the rest of the progam can continue to run'
    program = Thread(target=serveCoordinates)
    program.start()

    'must wait for the server to be up in order to make request then save coordinates into a list'
    time.sleep(3)
    'makes request and saves it as a list of floats in the form [Lat1, Long1, Lat2,  Long2...]'
    r = requests.get("http://localhost:8000")
    coordList = [float(x) for x in r.text.split()]
    'convert coordinates to utm'
    utmList = toUtm(coordList)
    'calculate the speed'
    averageSpeed = calculateSpeed(utmList)
    print("the average speed is " + str(averageSpeed) + " meters per second")
    return averageSpeed


'''
serves coordinates locally using localport:8000
Creates a request handler that handles GET request
returns the file at the path coordinate.text
file will be returned in the form of a string
'''
def serveCoordinates():
    PORT = 8000
    print("starting up server")

    class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/':
                self.path = 'coordinates.txt'
            return http.server.SimpleHTTPRequestHandler.do_GET(self)


    handler_object = MyHttpRequestHandler

    my_server = socketserver.TCPServer(("", PORT), handler_object)
    my_server.serve_forever()


'''
    Uses the function utm.from_latlon to get the utm coordinates of all the points
    returns a list of tuples representing (easting, northing)
'''
def toUtm(coordList):
    utmList = []
    for element in coordList:
        index = coordList.index(element)
        if index % 2 == 0:
            utmCoord = utm.from_latlon(element, coordList[index+1])
            utmList.append((utmCoord[0], utmCoord[1]))
    return utmList


'''
    caclulates the average speed of a series of utm coordinate points
    distance between two utm points is approximated by sqrt((E1-E2)^2+(N1-N2)^2)
    where E is easting and N is northing
'''
def calculateSpeed(coordList):
    totalDistance = 0.0
    'set time to -1'
    'the time will be larger then one because one second will be added on the final coordinate point'
    totalTime = -1
    for coord1 in coordList:
        index = coordList.index(coord1)
        totalTime += 1
        coord2 = coordList[index + 1]
        distance = math.sqrt(math.pow( (coord1[0] - coord2[0]) , 2) + math.pow( (coord1[1] - coord2[1]) ,2))
        'current speed is distance divided by time (which is one second)'
        totalDistance += distance

    return totalDistance / totalTime

main()
