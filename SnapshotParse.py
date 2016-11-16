__author__ = 'Cjones'
from xml.dom import minidom
import math

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




xmldoc = minidom.parse("snapshot.xcm")

snapshot = xmldoc.getElementsByTagName("snapshot")[0]

ENB = snapshot.getElementsByTagName("ENBEquipment")

PCItext = open('pcitext.csv', 'w')
kml = open('LTESnap.kml', 'w')
#This is just stuff that must go into every KML
kml.write("<?xml version='1.0' encoding='UTF-8'?>\n")
kml.write("<kml xmlns='http://earth.google.com/kml/2.1'>\n")
kml.write("<Document>\n")
#This is what the kml file will show up named as in Google Earth
kml.write("\t<name>LTESnap</name>\n")

#Set Style
kml.write("\t<Style id='LTE'>\n")
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
kml.write("\t\t<name>LTE</name>\n")
kml.write("\t\t<open>1</open>\n")



#Gets information from ENB
for ENBEquipment in ENB:
    name = ENBEquipment.attributes["id"]
    name1 = name.value
    print(name1)
    PCItext.write('\n' + str(name1) + ',')
    siteid = name1[0:6]
    print(siteid)
    sitehex = hex(int(siteid))
    sitehex = sitehex[2:7]
    print(sitehex)
    latitudeEL = ENBEquipment.getElementsByTagName("bbuConfiguredPositionLatitude")[0]
    longitudeEL = ENBEquipment.getElementsByTagName("bbuConfiguredPositionLongitude")[0]
    latitude = float(latitudeEL.firstChild.data)
    longitude = float(longitudeEL.firstChild.data)
    lat, lon = sectordraw(latitude, longitude, 276)
    print(str(latitude) + ',' + str(longitude))
    antenna = ENBEquipment.getElementsByTagName("AntennaPort")
    kml.write("\t\t<Folder>\n")
    kml.write("\t\t\t<name>" + name1 + "</name>\n")
    kml.write("\t\t\t<open>0</open>\n")

# Gets information out of the Antenna Ports
    for AntennaPort in antenna:
        sector = AntennaPort.attributes["id"]
        sector1 = sector.value
        #print(sector1)
        if int(sector1) == 1:
            azimuthEl = AntennaPort.getElementsByTagName("azimuth")[0]
            azimuth = azimuthEl.firstChild.data
            azimuth1 = '{0:.0f}'.format(float(azimuth))
            azimuth1 = int(azimuth1)
            try:
                labelEL = AntennaPort.getElementsByTagName("antennaLabel")[0]
                label = labelEL.firstChild.data
            except:
                pass
            #alpha = 0
            #beta = 0
            #gamma = 0
            if label in ["Red/Red", "RED/ ORANGE", "Ant_1_1", "Alpha_1", "Alpha"]:
                name2 = "Alpha LTE"
                print(name2)
                print(azimuth1)
                alpha = azimuth1
                styleid = 'inline0'
                becid = sitehex + '01'
                ENB0 = ENBEquipment.getElementsByTagName("Enb")
                try:
                    for Enb in ENB0:
                        LTEC = Enb.getElementsByTagName("LteCell")[0]
                        pci = LTEC.getElementsByTagName("pci")[0]
                        pci1 = pci.firstChild.nodeValue
                        PCItext.write(pci1 + ',')
                        print(pci1)
                except:
                    print("no pci found")
                for Enb in ENB0:
                    #Get eUTRA neighbors
                    nbr = []
                    Unbr = []
                    try:
                        LTEC = Enb.getElementsByTagName("LteCell")[0]
                        LTEN = LTEC.getElementsByTagName("LteNeighboringCellRelation")
                        for LteNeighboringCellRelation in LTEN:
                            neighbor = LteNeighboringCellRelation.attributes["id"]
                            neighbor1 = neighbor.firstChild.nodeValue
                            #print(neighbor1)
                            nbr.append(neighbor1)
                    except:
                        print("No Cell")
                    #Get UTRA neighbors
                    try:
                        LTEC = Enb.getElementsByTagName("LteCell")[0]
                        UTRAN = LTEC.getElementsByTagName("UtraFddNeighboringCellRelation")
                        for UtraFddNeighboringCellRelation in UTRAN:
                            neighborU = UtraFddNeighboringCellRelation.attributes["id"]
                            neighborU1 = neighborU.firstChild.nodeValue
                            #print(neighbor1)
                            Unbr.append(neighborU1)
                    except:
                        print("No Cell")
                try:
                    for Enb in ENB0:
                        LTEC = Enb.getElementsByTagName("LteCell")[0]
                        CRadius = LTEC.getElementsByTagName("cellRadius")[0]
                        CRadius1 = CRadius.firstChild.nodeValue
                        print(CRadius1)
                except:
                    print("no Cell Radius found")
            elif label in ["Yellow/Yellow", "Ant_2_1", "Beta_1", "BLUE/ ORANGE", "Beta"]:
                name2 = "Beta LTE"
                print(name2)
                print(azimuth1)
                beta = azimuth1
                styleid = 'inline1'
                becid = sitehex + '02'
                ENB0 = ENBEquipment.getElementsByTagName("Enb")
                try:
                    for Enb in ENB0:
                        LTEC = Enb.getElementsByTagName("LteCell")[1]
                        pci = LTEC.getElementsByTagName("pci")[0]
                        pci1 = pci.firstChild.nodeValue
                        PCItext.write(pci1 + ',')
                        print(pci1)
                except:
                    print("no pci found")
                for Enb in ENB0:
                    nbr = []
                    Unbr = []
                    try:
                        LTEC = Enb.getElementsByTagName("LteCell")[1]
                        LTEN = LTEC.getElementsByTagName("LteNeighboringCellRelation")
                        for LteNeighboringCellRelation in LTEN:
                            neighbor = LteNeighboringCellRelation.attributes["id"]
                            neighbor1 = neighbor.firstChild.nodeValue
                            #print(neighbor1)
                            nbr.append(neighbor1)
                    except:
                        print("No Cell")
                    #Get UTRA neighbors
                    try:
                        LTEC = Enb.getElementsByTagName("LteCell")[1]
                        UTRAN = LTEC.getElementsByTagName("UtraFddNeighboringCellRelation")
                        for UtraFddNeighboringCellRelation in UTRAN:
                            neighborU = UtraFddNeighboringCellRelation.attributes["id"]
                            neighborU1 = neighborU.firstChild.nodeValue
                            #print(neighbor1)
                            Unbr.append(neighborU1)
                    except:
                        print("No Cell")
                try:
                    for Enb in ENB0:
                        LTEC = Enb.getElementsByTagName("LteCell")[1]
                        CRadius = LTEC.getElementsByTagName("cellRadius")[0]
                        CRadius1 = CRadius.firstChild.nodeValue
                        print(CRadius1)
                except:
                    print("no Cell Radius found")
                print(nbr)
            elif label in ["Purple/Purple", "Ant_3_1", "Gamma_1", "GREEN/ORANGE", "Gamma"]:
                name2 = "Gamma LTE"
                print(azimuth1)
                gamma = azimuth1
                styleid = 'inline2'
                becid = sitehex + '03'
                ENB0 = ENBEquipment.getElementsByTagName("Enb")
                try:
                    for Enb in ENB0:
                        LTEC = Enb.getElementsByTagName("LteCell")[2]
                        pci = LTEC.getElementsByTagName("pci")[0]
                        pci1 = pci.firstChild.nodeValue
                        PCItext.write(str(pci1) + ',')
                        print(pci1)
                except:
                    print("no pci found")
                for Enb in ENB0:
                    nbr = []
                    Unbr = []
                    try:
                        LTEC = Enb.getElementsByTagName("LteCell")[2]
                        LTEN = LTEC.getElementsByTagName("LteNeighboringCellRelation")
                        for LteNeighboringCellRelation in LTEN:
                            neighbor = LteNeighboringCellRelation.attributes["id"]
                            neighbor1 = neighbor.firstChild.nodeValue
                            #print(neighbor1)
                            nbr.append(neighbor1)
                    except:
                        print("No Cell")
                    #Get UTRA neighbors
                    try:
                        LTEC = Enb.getElementsByTagName("LteCell")[2]
                        UTRAN = LTEC.getElementsByTagName("UtraFddNeighboringCellRelation")
                        for UtraFddNeighboringCellRelation in UTRAN:
                            neighborU = UtraFddNeighboringCellRelation.attributes["id"]
                            neighborU1 = neighborU.firstChild.nodeValue
                            print(neighborU1)
                            Unbr.append(neighborU1)
                    except:
                        print("No Cell")
                try:
                    for Enb in ENB0:
                        LTEC = Enb.getElementsByTagName("LteCell")[2]
                        CRadius = LTEC.getElementsByTagName("cellRadius")[0]
                        CRadius1 = CRadius.firstChild.nodeValue
                        print(CRadius1)
                except:
                    print("no Cell Radius found")
            lat, lon = sectordraw(latitude, longitude, azimuth1)
            print(str(lat) + ', ' + str(lon))
            kml.write("\t\t\t<Placemark>\n")
            kml.write("\t\t\t\t<name>" + name2 + "</name>\n")
            kml.write("\t\t\t\t<description>" + name1 + '\n' +
                      "Azimuth: " + str(azimuth1) + '\n' +
                      "Sector ID (BEC): " + becid + '\n' +
                      "PCI: " + str(pci1) + '\n' +
                      "Cell Radius: " + str(CRadius1) + " km" + '\n\n' +
                      "LTE Neighbors: \n")
            try:
                for x in nbr:
                    kml.write(x + '\n')
            except:
                print("No Neighbors found")
            kml.write("\n\n UMTS Neighbors: \n")
            try:
                for x in Unbr:
                    kml.write(x + '\n')
            except:
                print("No Neighbors Found")
            kml.write("\t\t\t\t</description>")
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
    kml.write("\t\t\t\t<styleUrl>#LTE</styleUrl>\n")
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
#print("CID finished")

    #ENBID = ENBEquipment.getElementsByTagName("Enb")[0]
    #print(ENBID)
    #LTECell = ENBID.getElementsByTagName("LTECell")[0]
    #print(LTECell)
    #Cellname = LTECell.attributes["id"]
    #Cellname1 = Cellname.value
    #CellID = int(Cellname1[-1])
    #print(CellID)