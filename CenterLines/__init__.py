# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CenterLines
                                 A QGIS plugin
 create centered lines out of points
                             -------------------
        begin                : 2017-04-12
        copyright            : (C) 2017 by ERVOLKT
        email                : volkertheil@googlemail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load CenterLines class from file CenterLines.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .center_lines import CenterLines
    return CenterLines(iface)
