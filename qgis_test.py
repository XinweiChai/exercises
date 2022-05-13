import os
from qgis.core import *

# Supply the path to the qgis install location
# QgsApplication.setPrefixPath("/usr/bin/qgis", True)
# Create a reference to the QgsApplication.
# Setting the second argument to True enables the GUI. We need
# this since this is a custom application.

qgs = QgsApplication([], True)
# load providers
qgs.initQgis()
# Write your code here to load some layers, use processing
# algorithms, etc.

from qgis.PyQt import QtGui

p = QgsProject.instance()
p.read('/home/chai/geohash3.qgz')

layers = p.mapLayersByName('group_6_comp_0_16_8_')
QgsProject.instance().layerTreeRoot().findLayer(layers[0]).setItemVisibilityChecked(True)
base_layer = p.mapLayersByName('Amap')[0]
QgsProject.instance().layerTreeRoot().findLayer(base_layer).setItemVisibilityChecked(True)
layer = layers[0]

manager = p.layoutManager()
layoutName = 'zgc'
layouts_list = manager.printLayouts()
for i in layouts_list:
    if i.name() == layoutName:
        manager.removeLayout(i)
layout = QgsPrintLayout(p)
layout.initializeDefaults()
layout.setName(layoutName)
manager.addLayout(layout)

map = QgsLayoutItemMap(layout)
map.setRect(2, 2, 2, 2)
# set the map extent
ms = QgsMapSettings()
ms.setLayers([layer])

# rect = QgsRectangle(ms.fullExtent())
rect = QgsRectangle(116.294857467, 40.028330539, 116.361690351, 40.065211782)
rect.scale(1.0)
# ms.setExtent(rect)
map.setExtent(rect)
layout.addLayoutItem(map)

# map.attemptMove(QgsLayoutPoint(5, 20, QgsUnitTypes.LayoutMillimeters))
map.attemptResize(QgsLayoutSize(297, 210, QgsUnitTypes.LayoutMillimeters))

base_path = os.path.join(QgsProject.instance().homePath())
pdf_path = os.path.join("output.pdf")

exporter = QgsLayoutExporter(layout)
exporter.exportToPdf(pdf_path, QgsLayoutExporter.PdfExportSettings())
# Finally, exitQgis() is called to remove the
# provider and layer registries from memory
qgs.exitQgis()
