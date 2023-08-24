import ase
import copy
import numpy as np


def build_atoms(data: dict) -> ase.Atoms:
    """ 
    Populate Atoms class with atoms in molecule.
        atoms.info : global variables
        atoms.array : variables for individual atoms
    """

    atoms = ase.atoms.Atoms(
        symbols=data['elements'],
        positions=data['positions']
    )
    atoms.info['energy'] = data['energy_internal_0K']
    #atoms.arrays['positions'] = data['positions']

    return copy.copy(atoms)
