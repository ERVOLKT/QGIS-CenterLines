# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CenterLines
                                 A QGIS plugin
 create centered lines out of points
                              -------------------
        begin                : 2017-04-12
        git sha              : $Format:%H$
        copyright            : (C) 2017 by ERVOLKT
        email                : volkertheil@googlemail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, QVariant

from PyQt4.QtGui import QAction, QIcon, QFileDialog
#need to be in there, for e.g. QgsFields or object or QgsVectorFileWriter:
from qgis.core import *
from qgis.gui import *

# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from center_lines_dialog import CenterLinesDialog
import os.path


class CenterLines:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'CenterLines_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = CenterLinesDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Qgis-CenterLines')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'CenterLines')
        self.toolbar.setObjectName(u'CenterLines')
        
        #for pushbutton path selection
        self.dlg.lineEdit.clear()
        self.dlg.pushButton.clicked.connect(self.select_output_file)

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('CenterLines', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        #self.dlg = CenterLinesDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/CenterLines/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'creates centered lines from points'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Qgis-CenterLines'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def select_output_file(self):
        filename = QFileDialog.getSaveFileName(self.dlg, "Select output file ","", '*.txt')
        self.dlg.lineEdit.setText(filename)

    def run(self):
        """Run method that performs all the real work
        """using the self.dlg.comboBox was a dead end, instead QgsMapLayerComboBox (automatically updated) will serve our needs better
       
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:

            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            """filename = self.dlg.lineEdit.text()
            output_file = open(filename, 'w')"""

            #specify selected layer in intelligent comboBox and translate it to iface layer index
            selectedLayerIndex = self.dlg.mMapLayerComboBox.currentIndex();
            print "selectedLayerIndex: ", selectedLayerIndex;
            layers = self.iface.legendInterface().layers();
            selectedLayer = layers[selectedLayerIndex]
            print "Selected layer's name: ",selectedLayer.name();
            """fields = selectedLayer.pendingFields()
            fieldnames = [field.name() for field in fields]

            for f in selectedLayer.getFeatures():
                line = ','.join(unicode(f[x]) for x in fieldnames) + '\n'
                unicode_line = line.encode('utf-8')
                output_file.write(unicode_line)
            output_file.close()"""

            if selectedLayer.type() == 0:
                print("selected layer type is Vector");
                #vectorlyr = l;
                geom_array = [];
                for f in selectedLayer.getFeatures():
                    geom = f.geometry().asPoint();
                    print(geom);
                    #add Points to array as QgsGeometry objects
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
                self.iface.addVectorLayer('GIS/Qgis_Plugins/CenterLines/project/lines.shp', "lines", "ogr");
            else:
                print("this part belongs to Raster");
        #dir(xyz) prints methods for any object


