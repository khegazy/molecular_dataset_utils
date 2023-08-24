import sys
import torch
import numpy as np

def parse_float(s: str) -> float:
    """ Converts string to float """
    try:
        return float(s)
    except ValueError:
        base, power = s.split('*^')
        return float(base) * 10**float(power)


def parse_int(s: str) -> int:
    """ Converts string to int """
    try:
        return int(s)
    except ValueError:
        print(s.split('*^'))
        base, power = s.split('*^')
        return int(float(base) * 10**float(power))


def parse_scalar(idx: int, value: str):
    """ Parses string according to type in QM9 Scalar Properties """
    if idx == 0:
        return value
    elif idx == 1:
        return parse_int(value)
    else:
        return parse_float(value)


def parse_scalar_properties(s_properties: str) -> dict:
    """ Parse QM9 Scalar Properties into a dictionary """
    property_names = [
        'tag', 'i', 'A', 'B', 'C', 'dipole', 'iso_polarizability',
        'energy_homo', 'energy_lumo', 'energy_gap', 'r2',
        'energy_zero_point', 'energy_internal_0K', 'energy_internal_298.15K',
        'enthalpy_298.15K', 'free_energy_298.15K', 'heat_capacity_298.15K'
    ]
    properties = s_properties.split('\t')
    properties = properties[0].split(' ') + properties[1:]
    dict_properties = {
        name : parse_scalar(idx, prop)
        for idx, (name, prop) in enumerate(zip(property_names, properties))
    }

    return dict_properties

	
def parse_position_charge(lines: list[str]):
    """ 
    Returns arrays for element type [N], xyz positions [N,3], and charges[N]
    from QM9 data lines
    """
    
    elements = [None,]*len(lines)
    positions = [None,]*len(lines)
    charges = [None,]*len(lines)
    for idx,line in enumerate(lines):
        element, x, y, z, charge = line.split()
        elements[idx] = element
        charges[idx] = parse_float(charge)
        positions[idx] = np.array([parse_float(pos) for pos in [x, y, z]])

    return np.array(elements),\
        np.array(positions, dtype=float),\
        np.array(charges, dtype=float)


def parse_xyz(filename: str):
    """
    Parses QM9 specific xyz files. See https://www.nature.com/articles/sdata201422/tables/2 for reference
    :param filename: str path to file
    :return:
    """

    data = None
    with open(filename, 'r') as xyz:
        lines = xyz.readlines()

        #try:
        # Scalar properties
        data = parse_scalar_properties(lines[1])
        # Number of atoms
        data['num_atoms'] = parse_int(lines[0])
        # Element type, xyz positions, partial charges
        data['elements'], data['positions'], data['charges'] =\
            parse_position_charge(lines[2:data['num_atoms']+2])
        # Harmonic oscillator frequencies
        data['harmonic_oscillator_frequencies'] =\
            np.array([
                parse_float(fr) for fr in lines[data['num_atoms']+2].split('\t')
            ])
        # SMILES strings
        data['smiles'] = np.array(
            lines[data['num_atoms']+3].split(), dtype=str)
        # InChI strings
        data['inchi'] = lines[data['num_atoms']+4].split()
        #except ValueError as err:
        #    print(F"ERROR on {filename}: {err}")
        #    sys.exit(1)


    return data 
