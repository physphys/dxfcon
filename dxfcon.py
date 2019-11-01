from decimal import Decimal, ROUND_HALF_UP
import dxfgrabber
import os
import sys
import tkinter.filedialog
import tkinter.messagebox


def select_dxf_file():
    root = tkinter.Tk()
    root.withdraw()
    fTyp = [("", "dxf")]
    iDir = os.path.abspath(os.path.dirname(__file__))
    file = tkinter.filedialog.askopenfilename(filetypes=fTyp, initialdir=iDir)
    return file


def sisyagonyu(points):
    x = Decimal(str(points[0])).quantize(
        Decimal('0.01'), rounding=ROUND_HALF_UP)
    y = Decimal(str(points[1])).quantize(
        Decimal('0.01'), rounding=ROUND_HALF_UP)
    return [x, y]


def make_con(points):
    with open('test.con', mode='w') as f:
        f.write(
            "PX60000;\n\nSZ0.6;\nR20.9000,0.9000;3.9000,3.9000;\nSI0;\nSJ0;\nST0;\n\n")
        for i, point in enumerate(points):
            x, y = point
            f.write("PCtest{0};\n{1},{2};\n".format(i + 1, x, y))
            f.write("PPtest{0};\n{1},{2};\n".format(i + 1, x, y))
            f.write("SI0;\nSJ0;\nST0;\n\n")
        f.write('!END')


def center_point(points):
    chip_size = 0.6  # mm
    return [point - (chip_size / 2) for point in map(max, zip(*points))]


def read_blocks(dxf_file_path, layer_name):
    dxf = dxfgrabber.readfile(dxf_file_path)
    block_entities = [entity for entity in dxf.entities if entity.dxftype ==
                      'LWPOLYLINE' and entity.layer == layer_name]
    center_points = [sisyagonyu(points)
                     for points in list(map(center_point, block_entities))]
    center_points.sort(key=lambda point: point[0])
    center_points.sort(key=lambda point: point[1])
    return center_points


def dxf_layers(dxf_file_path):
    dxf = dxfgrabber.readfile(dxf_file_path)
    return [layer.name for layer in dxf.layers]


file = select_dxf_file()
# select_layer(dxf_layers(file))
# layer_name = select_layer(dxf_layers(file))
# make_con(read_blocks(file, layer_name))
