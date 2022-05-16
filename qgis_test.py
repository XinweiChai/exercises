import os
from pathlib import Path

from PyQt5.QtCore import QTimer
from qgis.core import *
from qgis.utils import iface

areas = {'zhongguancun': [116.298883030, 39.968187255, 116.362757154, 40.003435727],
         'xierqi': [116.294857467, 40.028330539, 116.361690351, 40.065211782],
         'wangfujing': [116.382217576, 39.891506917, 116.446091700, 39.926755390],
         'shichahai': [116.362443277, 39.929737229, 116.426317401, 39.964985701]}
home = '/home/chai/Desktop/postdoc_report/Figures/'
directory = home + 'NCP/'
base_dir = home + 'base/'


def output_map(area_name):
    p = QgsProject.instance()
    p.read('/home/chai/geohash4.qgz')

    manager = p.layoutManager()
    layoutName = 'out'
    layouts_list = manager.printLayouts()
    for i in layouts_list:
        if i.name() == layoutName:
            manager.removeLayout(i)
    layout = QgsPrintLayout(p)
    layout.initializeDefaults()

    # pc = layout.pageCollection()
    # pc.pages()[0].setPageSize('A4', QgsLayoutItemPage.Orientation.Landscape)

    layout.setName(layoutName)
    manager.addLayout(layout)

    map_l = QgsLayoutItemMap(layout)
    map_l.setRect(2, 2, 2, 2)
    # set the map extent
    ms = QgsMapSettings()
    # rect = QgsRectangle(ms.fullExtent())
    rect = QgsRectangle(*areas[area_name])
    rect.scale(1.0)
    # ms.setExtent(rect)
    map_l.setExtent(rect)
    layout.addLayoutItem(map_l)

    Path(directory + area_name).mkdir(parents=True, exist_ok=True)
    exporter = QgsLayoutExporter(layout)

    for layer in p.mapLayers().values():
        name = layer.name()
        p.layerTreeRoot().findLayer(layer).setItemVisibilityChecked(True)
        ms.setLayers([layer])
        # map_l.attemptMove(QgsLayoutPoint(5, 20, QgsUnitTypes.LayoutMillimeters))
        map_l.attemptResize(QgsLayoutSize(297, 210, QgsUnitTypes.LayoutMillimeters))

        # base_path = os.path.join(p.homePath())
        if name == 'Amap':
            pdf_path = os.path.join(base_dir, 'base_' + f'{area_name}.pdf')
        else:
            pdf_path = os.path.join(directory + area_name, f"{name}.pdf")

        exporter.exportToPdf(pdf_path, QgsLayoutExporter.PdfExportSettings())
        p.layerTreeRoot().findLayer(layer).setItemVisibilityChecked(False)


def add_opacity(path):
    for i in os.listdir(path):
        if os.path.splitext(i)[1] == '.pdf':
            x = os.path.join(path, i)
            os.system(
                f'inkscape --actions="select-by-id:g10;object-set-property:opacity,0.5;export-filename:{x};export-do" {x}')


def add_layers():
    filePath = '/home/chai/Downloads/out/'

    prefixes = []
    count = 0

    # scale = 640
    layers = []
    for layer in QgsProject.instance().mapLayers().values():
        # layers.append(layer)
        # print(layer.id())
        print(layer.name())
        prefixes.append(layer.name())

    # print(layers[0].extent())
    # map.setExtent(layers[0].extent())
    # map.setRect(20, 20, 20, 20)

    def prepareMap():
        # layers = []
        layers = QgsProject.instance().mapLayers()

        for layer in layers:
            QgsProject.instance().layerTreeRoot().findLayer(layer).setItemVisibilityChecked(False)

        exportLayers = []
        for layer in QgsProject.instance().mapLayers().values():
            if layer.name().startswith(prefixes[count]):
                QgsProject.instance().layerTreeRoot().findLayer(layer).setItemVisibilityChecked(True)
                # iface.actionZoomToSelected().trigger()
                # qgis.utils.iface.mapCanvas().zoomScale(scale)

        QTimer.singleShot(1000, exportMap)

    def exportMap():  # Save as a PNG
        global count
        project = QgsProject.instance()
        l = QgsLayout(project)
        l.initializeDefaults()
        iface.mapCanvas().saveAsImage(filePath + prefixes[count] + ".png")
        print("Layer", prefixes[count], "exported")
        if count < len(prefixes) - 1:
            QTimer.singleShot(1000, prepareMap)
        count += 1

    prepareMap()


if __name__ == '__main__':
    qgs = QgsApplication([], True)
    qgs.initQgis()
    for i in areas:
        output_map(i)
        add_opacity(directory + i)
    qgs.exitQgis()
