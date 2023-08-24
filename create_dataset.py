import argparse
import glob
import ase
import ase.io
import numpy as np
from modules.parse_QM9 import parse_xyz
from modules.data_to_atoms import build_atoms

parser = argparse.ArgumentParser(description='Parsing and partitioning QM9.')
parser.add_argument('--xyz_folder', type=str, 
    default='/pscratch/sd/k/khegazy/datasets/QM9/datasets/raw_xyz/',
    help='Folder for xyz files')
parser.add_argument('--output_folder', type=str, 
    default='/pscratch/sd/k/khegazy/datasets/QM9/datasets/',
    help='Folder to output dataset')
parser.add_argument('--filename', type=str, 
    required=True,
    help='Folder for xyz files')
parser.add_argument('--data_split_ratio', nargs=3, type=float, 
    default=(0.6, 0.2, 0.2),
    help='Ratios of to split dataset (train, validation, test)')
parser.add_argument('--size', type=int, 
    default=None,
    help='Number of molecules in output')


if __name__ == '__main__':
    args = parser.parse_args()

    xyz_files = glob.glob(args.xyz_folder + "/*xyz")
    np.random.shuffle(xyz_files)
    atoms_list = []

    if args.size is not None:
        # Create dataset with set number of molecules
        atoms_list = [
            build_atoms(parse_xyz(xyz)) for xyz in xyz_files[:args.size]
        ]
        ase.io.write(
            F"{args.output_folder}/{args.filename}.xyz",
            atoms_list,
            format="extxyz"
        )

    else:
        # Create dataset split into train, validation, and tests
        assert np.sum(args.data_split_ratio) <= 1
        print("Splitting dataset into train/valid/test : {}/{}/{}".format(
            *args.data_split_ratio))
        idx1 = int(len(xyz_files)*args.data_split_ratio[0])
        idx2 = idx1 + int(len(xyz_files)*args.data_split_ratio[1])
        idx3 = int(len(xyz_files)*np.sum(args.data_split_ratio))
        loop_args = [
            ('train', (0, idx1)),
            ('valid', (idx1, idx2)),
            ('test', (idx2, idx3))
        ]
        for dataset, (idxI, idxF) in loop_args:
            atoms_list = [
                build_atoms(parse_xyz(xyz)) for xyz in xyz_files[idxI:idxF]
            ]
            ase.io.write(
                F"{args.output_folder}/{args.filename}_{dataset}.xyz",
                atoms_list,
                format="extxyz"
            )
