import numpy as np
import os
import argparse
import pyvista as pv

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--in-dir", type=str, default="../cortical", help="Input Surface Directory")
    parser.add_argument("--in-txt", type=str, default="../cortical/values.txt", help="Input Surface Directory")
    parser.add_argument("--out-dir", type=str, default="../cortical", help="Output Surface Directory")

    args = parser.parse_args()

    return args


def mapping(file, values):
    surface_data = pv.read(file)
    labels = np.unique(surface_data['label'])

    label_dict = {}
    for label in labels:
        label_id = int(label % 100)

        if 42 > label_id > 0:
            label_dict[label] = values[label_id - 1]
        elif label_id > 42:
            label_dict[label] = values[label_id - 2]
        elif label_id == 0 or label_id == 42:
            label_dict[label] = 0

    surface_data['label'] = np.array(list(map(lambda x: label_dict[x], surface_data['label'].tolist())))

    return surface_data


def main(name):
    if not os.path.isdir(args.out_dir):
        os.mkdir(args.out_dir)

    values = np.loadtxt(args.in_txt)
    input_files = os.listdir(args.in_dir)

    for file in input_files:
        if file.startswith("lh") and file.endswith("_labeled.vtk"):
            surface_data = mapping(os.path.join(args.in_dir, file), values[:74])
            surface_data.save(os.path.join(args.out_dir, f'lh_relabeled.vtk'), binary=False)

        elif file.startswith("rh") and file.endswith("_labeled.vtk"):
            surface_data = mapping(os.path.join(args.in_dir, file), values[74:])
            surface_data.save(os.path.join(args.out_dir, f'rh_relabeled.vtk'), binary=False)


if __name__ == '__main__':
    args = get_args()
    main(args)