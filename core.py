#for now, the core function is intended to work solely within the qgis python console

for l in iface.legendInterface().layers():
	layerType=l.type();
	if layerType == 0:
			print("Vektor");
			vectorlyr = l;
			geom_array = [];
			for f in vectorlyr.getFeatures():
				geom = f.geometry();
				print(geom.asPoint());
				#add POints to array as QgsGeometry objects
				geom_array.append(geom);
			print(geom_array);
	else:
		print("this part belongs to Raster");

#z.B. 
#iface.addVectorLayer('GIS/Qgis_Plugins/CenterLines/project/points.shp', "points", "ogr")

#dir(xyz) druckt die Objekt-Methoden