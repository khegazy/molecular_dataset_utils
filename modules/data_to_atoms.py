import ase
import copy
import numpy as np


def build_atoms(data: dict,
                elements: str,
                positions: str,
                energy: str = None,
                forces: str = None) -> ase.Atoms:
    """ 
    Populate Atoms class with atoms in molecule.
        atoms.info : global variables
        atoms.array : variables for individual atoms
    """

    atoms = ase.atoms.Atoms(
        symbols=data[elements],
        positions=data[positions]
    )
    if energy is not None:
        atoms.info['energy'] = data[energy]
    if forces is not None:
        atoms.info['forces'] = data[forces]
        
    return copy.copy(atoms)