#for now, the core function is intended to work solely within the qgis python console
# import modules for creation of vector files...
from PyQt4.QtCore import QVariant;

#this will attempt to create lines for any vector layer!!
for l in iface.legendInterface().layers():
	layerType=l.type();
	if layerType == 0:
			print("Vektor");
			vectorlyr = l;
			geom_array = [];
			for f in vectorlyr.getFeatures():
				geom = f.geometry().asPoint();
				print(geom);
				#add POints to array as QgsGeometry objects
				geom_array.append(geom);

			# define fields for feature attributes. A QgsFields object is needed
			fields = QgsFields()
			fields.append(QgsField("id", QVariant.Int))
			#fields.append(QgsField("second", QVariant.String))

			""" create an instance of vector file writer, which will create the vector file.
			Arguments:
			1. path to new file (will fail if exists already)
			2. encoding of the attributes
			3. field map
			4. geometry type - from WKBTYPE enum
			5. layer's spatial reference (instance of
			   QgsCoordinateReferenceSystem) - optional
			6. driver name for the output file """

			# create a linestring feature, in WebMercator here, has to be adapted lateron
			# vector linestring layer takes first point geometry & combines it w/ all other points
			writer = QgsVectorFileWriter("GIS/Qgis_Plugins/CenterLines/project/lines.shp", "CP1250", fields, QGis.WKBLineString, QgsCoordinateReferenceSystem(3857, QgsCoordinateReferenceSystem.PostgisCrsId), "ESRI Shapefile")
			if writer.hasError() != QgsVectorFileWriter.NoError:
			    print "Error when creating shapefile: ",  writer.errorMessage()

			for features in range(1,len(geom_array)):
				# add a feature
				fet = QgsFeature()
				 # add feature geometry attributes
				fet.setGeometry(QgsGeometry.fromPolyline([QgsPoint(geom_array[0]), QgsPoint(geom_array[features])]))
				#fet.setGeometry(QgsGeometry.fromPoint(QgsPoint(10,10)))
				 # add non-geo attributes
				fet.setAttributes([features, "text"])
				writer.addFeature(fet)

			# delete the writer to flush features to disk
			del writer

			#add new layer to TOC -- has to be changed lateron, this is not valid from within a plugin(?)
			iface.addVectorLayer('GIS/Qgis_Plugins/CenterLines/project/lines.shp', "lines", "ogr");
						

	else:
		print("this part belongs to Raster");

#dir(xyz) prints methods for any object

