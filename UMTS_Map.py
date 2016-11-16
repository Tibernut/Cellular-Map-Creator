__author__ = 'Cjone'
import math
from xml.dom import minidom


#generates end GPS coords for azimuth lines if given starting point and azimuth
def sectordraw(lat1, lon1, azimuth):
    d = 1.61
    R = 6378.14
    brng = azimuth * (math.pi/180)
    latitude1 = lat1 * (math.pi/180)
    longitude1 = lon1 * (math.pi/180)
    latitude2 = math.asin(math.sin(latitude1)*math.cos(d/R) + math.cos(latitude1)*math.sin(d/R)*math.cos(brng))
    longitude2 = longitude1 + math.atan2(math.sin(brng)*math.sin(d/R)*math.cos(latitude1),math.cos(d/R)-math.sin(latitude1)*math.sin(latitude2))
    latitude2 = latitude2 * (180/math.pi)
    longitude2 = longitude2 * (180/math.pi)
    return (latitude2, longitude2)

xmldoc = minidom.parse("UMTSsnapshot.xcm")
snapshot = xmldoc.getElementsByTagName("snapshot")[0]

kml = open('UMTSsnap.kml', 'w')
info = open('test.csv', 'w')
#This is just stuff that must go into every KML
kml.write("<?xml version='1.0' encoding='UTF-8'?>\n")
kml.write("<kml xmlns='http://earth.google.com/kml/2.1'>\n")
kml.write("<Document>\n")
#This is what the kml file will show up named as in Google Earth
kml.write("\t<name>UMTSsnap</name>\n")

#Set Style
kml.write("\t<Style id='UMTS'>\n")
kml.write("\t\t<LabelStyle>\n")
kml.write("\t\t\t<scale>0.8</scale>\n")
kml.write("\t\t\t<color>ffffffff</color>\n")
kml.write("\t\t</LabelStyle>\n")
kml.write("\t\t<IconStyle>\n")
#"..ff" sets the opacity to 100%
#kml.write("\t\t\t<color>ff000000</color>\n")
kml.write("\t\t\t<scale>1.2</scale>\n")
kml.write("\t\t\t<Icon>\n")
kml.write("\t\t\t\t<href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href>\n")
kml.write("\t\t\t</Icon>\n")
kml.write("\t\t</IconStyle>\n")
kml.write("\t</Style>\n")
kml.write("\t<Style id='inline0'>\n")
kml.write("\t\t<LineStyle>\n")
kml.write("\t\t\t<color>ff0000ff</color>\n")
kml.write("\t\t\t<width>2</width>\n")
kml.write("\t\t</LineStyle>\n")
kml.write("\t</Style>\n")
kml.write("\t<Style id='inline1'>\n")
kml.write("\t\t<LineStyle>\n")
kml.write("\t\t\t<color>ff00ffff</color>\n")
kml.write("\t\t\t<width>2</width>\n")
kml.write("\t\t</LineStyle>\n")
kml.write("\t</Style>\n")
kml.write("\t<Style id='inline2'>\n")
kml.write("\t\t<LineStyle>\n")
kml.write("\t\t\t<color>ffff00ff</color>\n")
kml.write("\t\t\t<width>2</width>\n")
kml.write("\t\t</LineStyle>\n")
kml.write("\t</Style>\n")
kml.write("\t<Folder>\n")
kml.write("\t\t<name>UMTS</name>\n")
kml.write("\t\t<open>1</open>\n")


info.write("Name,CID,Azimuth,Scrambling Code,Lat,Long,Freq,Antenna Height\n")
Sname = snapshot.getElementsByTagName("Site")
for Site in Sname:
    name = Site.attributes["id"]
    name1 = name.value
    print(name1)
    latitudeEL = Site.getElementsByTagName("latitude")[0]
    latitude = float(latitudeEL.firstChild.nodeValue)
    print(latitude)
    longitudeEL = Site.getElementsByTagName("longitude")[0]
    longitude = float(longitudeEL.firstChild.nodeValue)
    print(longitude)
    kml.write("\t\t<Folder>\n")
    kml.write("\t\t\t<name>" + name1 + "</name>\n")
    kml.write("\t\t\t<open>0</open>\n")

    NB = snapshot.getElementsByTagName("NodeB")
    for NodeB in NB:
        checkname = NodeB.attributes["id"]
        checkname1 = checkname.value
        #print(checkname1)


        if checkname1 == name1:

            Cell = NodeB.getElementsByTagName("FDDCell")
            Scramble = []
            for FDDCell in Cell:
                dlfreqEL = FDDCell.getElementsByTagName("dlFrequencyNumber")[0]
                #for z in dlfreqEL:
                dlfreq = dlfreqEL.firstChild.data
                print(str(dlfreq))
                nbr = []
                Gnbr = []
                CID = FDDCell.attributes["id"]
                CID1 = CID.value
                CID2 = CID1[-1:]
                print(CID1, CID2)
                if CID2 == "0":
                    Scram = FDDCell.getElementsByTagName("primaryScramblingCode")[0]
                    Scramfriendly = Scram.firstChild.nodeValue
                    Scram1 = str("Primary Scrambling Code: " + Scram.firstChild.nodeValue)
                    AheightEL = FDDCell.getElementsByTagName("antennaHeight")[0]
                    Aheight = AheightEL.firstChild.nodeValue
                    print("antennal Height=" + Aheight)
                    #Scramble = Scramble.append(Scram0)
                    #print(Scram1)
                    UMTSNbr = FDDCell.getElementsByTagName("UMTSFddNeighbouringCell")
                    GSMNbr = FDDCell.getElementsByTagName("GsmNeighbouringCell")
                    for UMTSFddNeighbouringCell in UMTSNbr:
                        neighbor =  UMTSFddNeighbouringCell.attributes["id"]
                        neighbor1 = neighbor.firstChild.nodeValue
                        nbr.append(neighbor1)
                    for GsmNeighbouringCell in GSMNbr:
                        neighbor =  GsmNeighbouringCell.attributes["id"]
                        neighbor1 = neighbor.firstChild.nodeValue
                        Gnbr.append(neighbor1)
                    styleid = "inline0"
                    name2 = "Alpha"
                    az = FDDCell.getElementsByTagName("azimuthAntennaAngle")[0]
                    azimuth = int(az.firstChild.nodeValue)
                    Cellid = FDDCell.getElementsByTagName("cellId")[0]
                    Cellid1 = Cellid.firstChild.nodeValue
                    print(azimuth)
                    info.write(checkname1+"_X,")
                    info.write(str(Cellid1) + ',' + str(azimuth) + ',' + str (Scramfriendly) + ',' + str(latitude) + ',' + str(longitude) + ',' + str(dlfreq) + ',' + str(Aheight) + '\n')
                    alpha = azimuth
                elif CID2 == "1":
                    UMTSNbr = FDDCell.getElementsByTagName("UMTSFddNeighbouringCell")
                    GSMNbr = FDDCell.getElementsByTagName("GsmNeighbouringCell")
                    Scram = FDDCell.getElementsByTagName("primaryScramblingCode")[0]
                    Scram1 = str("Primary Scrambling Code: " + Scram.firstChild.nodeValue)
                    AheightEL = FDDCell.getElementsByTagName("antennaHeight")[0]
                    Aheight = AheightEL.firstChild.nodeValue
                    #print(Scram1)
                    #Scramble = Scramble.append(Scram1)
                    for UMTSFddNeighbouringCell in UMTSNbr:
                        neighbor =  UMTSFddNeighbouringCell.attributes["id"]
                        neighbor1 = neighbor.firstChild.nodeValue
                        nbr.append(neighbor1)
                    for GsmNeighbouringCell in GSMNbr:
                        neighbor =  GsmNeighbouringCell.attributes["id"]
                        neighbor1 = neighbor.firstChild.nodeValue
                        Gnbr.append(neighbor1)
                    styleid = "inline1"
                    name2 = "Beta"
                    az = FDDCell.getElementsByTagName("azimuthAntennaAngle")[0]
                    azimuth = int(az.firstChild.nodeValue)
                    Cellid = FDDCell.getElementsByTagName("cellId")[0]
                    Cellid1 = Cellid.firstChild.nodeValue
                    print(azimuth)
                    info.write(checkname1+"_Y,")
                    info.write(str(Cellid1) + ',' + str(azimuth) + ',' + str (Scramfriendly) + ',' + str(latitude) + ',' + str(longitude) + ',' + str(dlfreq) + ',' + str(Aheight) + '\n')
                    beta  = azimuth
                elif CID2 == "2":
                    UMTSNbr = FDDCell.getElementsByTagName("UMTSFddNeighbouringCell")
                    GSMNbr = FDDCell.getElementsByTagName("GsmNeighbouringCell")
                    Scram = FDDCell.getElementsByTagName("primaryScramblingCode")[0]
                    Scram1 = str("Primary Scrambling Code: " + Scram.firstChild.nodeValue)
                    AheightEL = FDDCell.getElementsByTagName("antennaHeight")[0]
                    Aheight = AheightEL.firstChild.nodeValue
                    #Scramble = Scramble.append(Scram2)
                    #print(Scram1)
                    for UMTSFddNeighbouringCell in UMTSNbr:
                        neighbor =  UMTSFddNeighbouringCell.attributes["id"]
                        neighbor1 = neighbor.firstChild.nodeValue
                        nbr.append(neighbor1)
                    for GsmNeighbouringCell in GSMNbr:
                        neighbor =  GsmNeighbouringCell.attributes["id"]
                        neighbor1 = neighbor.firstChild.nodeValue
                        Gnbr.append(neighbor1)
                    styleid = "inline2"
                    name2 = "Gamma"
                    az = FDDCell.getElementsByTagName("azimuthAntennaAngle")[0]
                    azimuth = int(az.firstChild.nodeValue)
                    Cellid = FDDCell.getElementsByTagName("cellId")[0]
                    Cellid1 = Cellid.firstChild.nodeValue
                    print(azimuth)
                    info.write(checkname1+"_Z,")
                    info.write(str(Cellid1) + ',' + str(azimuth) + ',' + str (Scramfriendly) + ',' + str(latitude) + ',' + str(longitude) + ',' + str(dlfreq) + ',' + str(Aheight) + '\n')
                    gamma = azimuth
                else:
                    gamma = "NA"
                print(Scram1)
                Scramble.append(Scram1)
                print(Scramble)
                #Scramble = Scramble.append(Scram1)
                #print(Scramble)
                #for y in Scramble:
                #    print(y)
                print(checkname1)
                lat, lon = sectordraw(latitude, longitude, azimuth)
                #print(str(lat) + ', ' + str(lon))
                kml.write("\t\t\t<Placemark>\n")
                kml.write("\t\t\t\t<name>" + name2 + "</name>\n")
                kml.write("\t\t\t\t<description>" + name1 + '\n\n' +
                          "Azimuth: " + str(azimuth) + '\n' +
                          "Cell ID: " + str(Cellid1) + '\n\n' +
                          Scram1 + '\n' +
                          "UMTS Neighbors: \n")
                try:
                    for x in nbr:
                        kml.write(x + '\n')
                except:
                    print("No Neighbors Found")
                kml.write("\n\n GSM Neighbors: \n")
                try:
                    for x in Gnbr:
                        kml.write(x + '\n')
                except:
                    print("No Neighbors Found")
                kml.write("\t\t\t\t</description>\n")
                kml.write("\t\t\t\t<styleUrl>#" + styleid + "</styleUrl>\n")
                kml.write("\t\t\t\t<LineString>\n")
                kml.write("\t\t\t\t\t<tessellate>1</tessellate>\n")
                kml.write("\t\t\t\t\t<coordinates>\n")
                kml.write("\t\t\t\t\t\t" + str(longitude) + ',' + str(latitude) + " " + str(lon) + ',' + str(lat) + '\n')
                kml.write("\t\t\t\t\t</coordinates>\n")
                kml.write("\t\t\t\t</LineString>\n")
                kml.write("\t\t\t</Placemark>\n")



    kml.write("\t\t\t<Placemark>\n")
    kml.write("\t\t\t\t<name>" + name1 + "</name>\n")
    try:
        kml.write("\t\t\t\t<description>Site Name: " + name1 +
                  '\n Lat, Long: ' + str(latitude) + ', ' + str(longitude) + '\n Alpha: ' + str(alpha) + '\n Beta: ' + str(beta) + '\n Gamma: ' + str(gamma) +
                  "</description>\n")
    except:
        print('not present')
    kml.write("\t\t\t\t<styleUrl>#UMTS</styleUrl>\n")
    kml.write("\t\t\t\t<Point>\n")
    kml.write("\t\t\t\t\t<coordinates>" + str(longitude) + "," + str(latitude) + "</coordinates>\n")
    kml.write("\t\t\t\t</Point>\n")
    kml.write("\t\t\t</Placemark>\n")
    kml.write("\t\t\t</Folder>\n")

#this needs to be at the end of every KML file
kml.write("\t\t</Folder>\n")
kml.write("</Document>\n")
kml.write("</kml>\n")
#close the file
kml.close()