import os
import pds4_tools as pds


def read_pds(root, tp):
    f_list = os.listdir(root)
    for f in f_list:
        if f.split('.')[-1] == tp:
            pds_struct = pds.read(root + f)
            pds.view(from_existing_structures=pds_struct)


def main():
    root = 'F://Download//'
    tp = '2CL'
    read_pds(root, tp)


main()
