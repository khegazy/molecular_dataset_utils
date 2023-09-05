import ase
import copy
import numpy as np


def build_atoms(data: dict
                energy: str = None,
                forces: str = None) -> ase.Atoms:
    """ 
    Populate Atoms class with atoms in molecule.
        atoms.info : global variables
        atoms.array : variables for individual atoms
        
    Both "energy" and "forces" are the dict strings in data.
    """

    atoms = ase.atoms.Atoms(
        symbols=data['elements'],
        positions=data['positions']
    )
    if energy is not None:
        atoms.info['energy'] = data[energy]
    if forces not None:
        atoms.info['forces'] = data[forces]
        
    return copy.copy(atoms)