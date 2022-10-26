import pyvista as pv
import numpy as np
import os
import argparse
from glob import glob

def get_args():
    parser = argparse.ArgumentParser()

    # Dataset & dataloader
    parser.add_argument("--in-dir", type=str, default="./surfaces_in", help="Input Surface Directory")
    parser.add_argument("--out-dir", type=str, default="./surfaces_out_all", help="Output Surface Directory")
    parser.add_argument("--labels", type=float, default=[11176, 11177, 11178, 11179, 11180, 11181,
                                                       12176, 12177, 12178, 12179, 12180, 12181], nargs="+",
                        help="New Labels")

    args = parser.parse_args()

    return args


def main(name):
    if not os.path.isdir(args.out_dir):
        os.mkdir(args.out_dir)

    # regions = ["sub_lh_amy", "sub_lh_caud", "sub_lh_hippo", "sub_lh_thal", "sub_lh_put", "sub_lh_gp",
    #            "sub_rh_amy", "sub_rh_caud", "sub_rh_hippo", "sub_rh_thal", "sub_rh_put", "sub_rh_gp"]

    label_ids = [11176, 11177, 11178, 11179, 11180, 11181, 12176, 12177, 12178, 12179, 12180, 12181]
    label_dict = {}
    
    for idx, label in enumerate(label_ids):
        label_dict[float(label)] = args.labels[idx]
    
    # for file in input_surface_files:
        
        # for idx, region in enumerate(regions):
        #     if region in file:
        #         region_name = region
        #         region_id = idx
        #         break

        #print(region_name)
    file  = args.in_dir
    surface_data = pv.read(file)
    surface_data['label'] = np.array(list(map(lambda x: label_dict[x], surface_data['label'].tolist())))

    surface_data.save(os.path.join(args.out_dir, f'sub_all_LMCI_relabeled.vtk'), binary=False)


if __name__ == '__main__':
    args = get_args()
    main(args)
