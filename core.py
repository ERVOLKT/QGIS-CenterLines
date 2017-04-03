#for now, the core function is intended to work solely within the qgis python console

for l in iface.legendInterface().layers():
	layerType=l.type();
	if layerType == 0:
			print("Vektor");
			vectorlyr = l;
			for f in vectorlyr.getFeatures():
				geom = f.geometry();
				print(geom.asPoint());

	else:
		print("this part belongs to Raster");
        
#layer erstellen
#???


#Geometrie erstellen
#z.B. gLine = QgsGeometry.fromPolyline([QgsPoint(1, 1), QgsPoint(2, 2)])
        
# dir() shows all object methods!!!
#print(dir(object));
