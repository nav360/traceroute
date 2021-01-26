# this will allow this program to interpret JSON object. See example JSON:http://dazzlepod.com/ip/128.173.239.242.json
import json

# the tools needed to access a URL and get data.
import urllib.request

# allows operations such opening a default browser at a given URL
import webbrowser, os

# for pausing our requests to a web service that takes IP and returns latitude,longitude
import time

# scapy is an extensive networking library for python. We are going to be using its 'traceroute()'
from scapy.layers.inet import socket
from scapy.layers.inet import traceroute

# this is to plot our lat/long data onto Google Maps  https://pypi.org/project/gmplot/
from gmplot import gmplot   

# adding for arguments
import sys 


# plots 3 coordinates onto Google Maps - hardcoded for in-class example
def plot_lat_long(latsCords: list, longsCords: list):   
    # the initial lat long and the zoom levels for the map (3 is zoomed out)
    gmap = gmplot.GoogleMapPlotter(0, 0, 3)
    
    #Handle path issue for windows, so that marker images can optionally be found using gmplot
    if ":\\" in gmap.coloricon:
        gmap.coloricon = gmap.coloricon.replace('/', '\\')
        gmap.coloricon = gmap.coloricon.replace('\\', '\\\\')
        
    
    # List of possible colors for the markers
    col = ['red', 'blue', 'yellow', 'green', 'gray', 'purple', 'c', 'm', 'white', 'orange', 'pink']
    # placing large dots on the lat longs
    # for your homework you will pass in coordinates retrieved from dazzlepod. 
    # for this in-class example, we will plot a hard-coded list of coordinates
    lats = latsCords
    longs = longsCords
    for x in range(len(lats)):
        y = x + 1
        z = x
        # This ensures that the color indexes are always in bouhd
        if z > 10 :
            z = z % 10
        gmap.marker(lats[x], longs[x], title = y, color = col[z]) 
        gmap.plot(lats, longs, 'cornflowerblue', edge_width = 2.5)

        

    # get the currentdirectory
    cwd = os.getcwd()
    
    # saving the map as an HTML into the project directory
    gmap.draw("traceroute.html")
    
    # opening the HTML via default browser
    webbrowser.open("file:///" + cwd +"/traceroute.html")


def find_and_plot_coordinates():
    # Houses the lats and longs coordinates
    latCords = []
    longCords = []
    
    for x in ips :
        # tool for finding latitutde and longitude of ip address
        url = "http://dazzlepod.com/ip/{}.json".format(x)
    
        # debugging the URLs
        print(url)
        response = urllib.request.urlopen(url)
        data = json.loads(response.read().decode())
        # making sure the wesbsite gave us lat and long
        if 'latitude' in data and 'longitude' in data:
            latCords.append(data['latitude'])
            longCords.append(data['longitude'])        
            # pausing for 2 seconds to make sure we don't get banned by 'dazzlepod.com'
            time.sleep(SLEEP_SECONDS)
        # This displays the longitude and lattitude data to the user.
        print(data)
    #calls function to plot the lats and longs
    plot_lat_long(latCords, longCords)



sys.argv
inp = str(sys.argv[1])
print(inp)

#will need to slow down the request frequency from 'dazzlepod.com' to find latitude and longitude
SLEEP_SECONDS = 2;
#hostname to traceroute to, hardcoded for in-class example
hostname = inp


# converting request hostname into IP address
ip = socket.gethostbyname(hostname)
    
# a good explanation of how traceroute works: https://www.youtube.com/watch?v=G05y9UKT69s
# add maxttl=100 or more if you want to traceroute even deeper.
#'res' -- results from traceroute 
res, _ = traceroute(ip,maxttl=64,verbose = 0)

# will store retrieved IPs here.
ips = []
# find the latitude and longitude 
# going through the traceroute results and extracting IP addresses into the array
for item in res.get_trace()[ip]:
    ips.append(res.get_trace()[ip][item][0])
    
find_and_plot_coordinates()