import glob
import argparse
import ase
import ase.io
import numpy as np
from modules.data_to_atoms import build_atoms
import os
from monty.serialization import loadfn


parser = argparse.ArgumentParser(description='Parsing and partitioning QM9.')
parser.add_argument('--data', type=str,
    help='Folder for the data')
parser.add_argument('--output_folder', type=str, 
    default='/pscratch/sd/m/mavaylon/sam_ldrd/radqm9/',
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

# This assumes that you have already untarred/unzipped the trajectories
base_dir = "/pscratch/sd/m/mavaylon/sam_ldrd/radqm9/radQM9/20230812_radQM9_trajectories"

# Get list of dictionaries of the data. Each dict is a molecule
data = loadfn(os.path.join(base_dir, "qm9pm3_trajectory_0.json"))

args = parser.parse_args()
if args.size is not None:
    # Create dataset with set number of molecules
    atoms_list = [
        build_atoms(data=molecule, elements='species', positions = 'geometries', energy='resp', forces='gradients') for molecule in data
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
    idx1 = int(len(data)*args.data_split_ratio[0])
    idx2 = idx1 + int(len(data)*args.data_split_ratio[1])
    idx3 = int(len(data)*np.sum(args.data_split_ratio))
    loop_args = [
        ('train', (0, idx1)),
        ('valid', (idx1, idx2)),
        ('test', (idx2, idx3))
    ]
    for dataset, (idxI, idxF) in loop_args:
        atoms_list = [
            build_atoms(data=molecule, elements='species', positions = 'geometries', energy='resp', forces='gradients') for molecule in data[idxI:idxF]
        ]
        ase.io.write(
            F"{args.output_folder}/{args.filename}_{dataset}.xyz",
            atoms_list,
            format="extxyz"
        )