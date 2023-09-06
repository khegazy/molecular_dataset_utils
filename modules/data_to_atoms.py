import ase
import copy
import numpy as np


def build_atoms(data: dict,
                elements: str,
                positions: (str, list),
                charge: int = None,
                spin: int = None,
                energy: str = None,
                forces: (str, list) = None,
                ) -> ase.Atoms:
    """ 
    Populate Atoms class with atoms in molecule.
        atoms.info : global variables
        atoms.array : variables for individual atoms
    """
    if isinstance(positions, str):
        positions=data[positions]
    else:
        positions = positions
    
    atoms = ase.atoms.Atoms(
        symbols=data[elements],
        positions=positions
    )
    if energy is not None:
        atoms.info['energy'] = data[energy]
    else:
        atoms.info['energy'] = 0 # TODO: energy needs to be updated when we get the new data.
    if forces is not None:
        if isinstance(forces, str):
            atoms.info['forces'] = data[forces]
        else :
            atoms.info['forces'] = forces
    if charge is not None:
        atoms.info['charge'] = data[charge]
    if spin is not None:
        atoms.info['spin'] = data[spin]
       
        
    return copy.copy(atoms)