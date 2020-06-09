import re
lat=" "
lon=" "
rssi=" "

fin = open("data.txt", "r")
fout = open("dataEnGPX.gpx", "w")

fout.write("<?xml version='1.0' ?>")
fout.write("\n<gpx xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' version='1.0' creator='William WS'>")
fout.write("\n  <trk>") 
fout.write("\n    <trkseg>")
    
for line in fin:
    lat = re.search(r"\(\([0-9]{1,2}[.][0-9]{,7}", line)
    if  lat :
        lat=lat.group().replace("((", "")
    else:
        lat=0
        
    lon = re.search(r"[ ][0-9]{1,2}[.][0-9]{,7}", line)
    if  lon :
        lon=lon.group()
    else:
        lon=0
    
    rssi = re.search(r"rssi=[-]?[0-9]{,4}", line)
    if  rssi :
        rssi=rssi.group().replace("rssi=", "").replace("-", "")
    else:
        rssi=0
        
    var="\n      <trkpt lat='"+str(lat)+"' lon='"+str(lon)+"'>"
    fout.write(str(var))
    var="\n        <ele>"+str(rssi)+"</ele>"
    fout.write(str(var))
    fout.write("\n      </trkpt>")

    #print("lat: ",str(lat))
    #print("lonn: ",str(lon))
    #print("rssi: ",str(rssi))
    
fout.write("\n    </trkseg>")
fout.write("\n  </trk>")
fout.write("\n</gpx>")

fin.close()
fout.close()

print("OK")

  
