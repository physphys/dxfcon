from decimal import Decimal, ROUND_HALF_UP
import dxfgrabber
import os
import sys
import tkinter.filedialog
from tkinter import *
from tkinter import ttk


def sisyagonyu(points):
    x = Decimal(str(points[0])).quantize(
        Decimal('0.01'), rounding=ROUND_HALF_UP)
    y = Decimal(str(points[1])).quantize(
        Decimal('0.01'), rounding=ROUND_HALF_UP)
    return [x, y]


def make_con(points, dir):
    with open(dir + '/' + 'generated.con', mode='w') as f:
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


def button_clicked(file, layer):
    dir = os.path.dirname(file)
    make_con(read_blocks(file, layer), dir)
    sys.exit()


root = tkinter.Tk()
root.withdraw()
fTyp = [("", "dxf")]
iDir = os.path.abspath(os.path.dirname(__file__))
file = tkinter.filedialog.askopenfilename(filetypes=fTyp, initialdir=iDir)


layers = dxf_layers(file)


root = tkinter.Tk()
root.title("Select layer")
frame = ttk.Frame(root, padding=10)
frame.grid()

combo_box = ttk.Combobox(frame)
combo_box['values'] = tuple(layers)
combo_box.set(layers[0])
combo_box.grid(row=0, column=0)

# Button
button = ttk.Button(
    frame, text='OK', command=lambda: button_clicked(file, combo_box.get()))
button.grid(row=0, column=1)
root.mainloop()
