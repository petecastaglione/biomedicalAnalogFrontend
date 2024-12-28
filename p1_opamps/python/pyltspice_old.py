# from pyltspice.ltspicebatch import simcommander
from PyLTSpice import SimCommander
from PyLTSpice.log.ltsteps import LTSpiceLogReader
import inspect
import re
import numpy as np
import os

class MOSFET:
    def __init__(self, name, model):
        self.name = name
        self.model = model
        self.Id = None
        self.Vgs = None
        self.Vds = None
        self.Vbs = None
        self.Vth = None
        self.Vdsat = None
        self.Gm = None
        self.Gds = None
        self.Gmb = None
        self.Cbd = None
        self.Cbs = None
        # self.Cgsov = None
        # self.Cgdov = None
        # self.Cgbov = None
        # self.dQgdVgb = None
        # self.dQgdVdb = None
        # self.dQgdVsb = None
        # self.dQddVgb = None
        # self.dQddVdb = None
        # self.dQddVsb = None
        # self.dQbdVgb = None
        # self.dQbdVdb = None
        # self.dQbdVsb = None
def parse_mosfet_data(log_file_path):
    mosfets = {}
    try:
        with open(log_file_path, 'r') as f:
            log_content = f.read()
    except FileNotFoundError:
        print(f"Error: Log file not found at {log_file_path}")
        return mosfets

    mosfet_data_start = log_content.find("--- BSIM3 MOSFETS ---")
    if mosfet_data_start == -1:
        print("No MOSFET data found in log file.")
        return mosfets

    mosfet_data = log_content[mosfet_data_start:]

    mosfet_blocks = re.findall(r"Name:\s*(.*?)\nModel:\s*(.*?)\n(.*?)(?=\n\n|\Z)", mosfet_data, re.DOTALL)

    for name_line, model_line, data_block in mosfet_blocks:
        names = [n.strip() for n in re.split(r"\s{2,}", name_line.replace("Name:", "").strip()) if n.strip()]
        models = [m.strip() for m in re.split(r"\s{2,}", model_line.replace("Model:", "").strip()) if m.strip()]
        num_mosfets = len(names)

        # Initialize MOSFET objects *before* parsing values
        for i in range(num_mosfets):
            mosfet = MOSFET(names[i], models[i])
            mosfets[mosfet.name] = mosfet

        data_lines = data_block.strip().split('\n')
        print(data_lines)
        param_names = [p.strip() for p in re.split(r"\s{2,}", data_lines[0].strip()) if p.strip()]

        for param_index, param_name in enumerate(param_names): #Iterate through the parameters
            try:
                values_line = data_lines[param_index+1] #Get the values line corresponding to the parameter
                values = [float(v.replace(",", ".")) for v in re.split(r"\s{2,}", values_line.strip())[1:] if v.strip()]
                for mosfet_index in range(num_mosfets): #Iterate through the mosfets
                    setattr(mosfets[names[mosfet_index]], param_name.replace(":", ""), values[mosfet_index])
            except (IndexError, ValueError) as e:
                print(f"Error parsing parameter {param_name}: {e}")
                continue
    return mosfets

def print_mosfet_parameter_by_name(mosfets, mosfet_name, parameter_name):
    """
    Prints a specific parameter for a given MOSFET name.

    Args:
        mosfets (dict): A dictionary of MOSFET objects, where keys are MOSFET names.
        mosfet_name (str): The name of the MOSFET.
        parameter_name (str): The name of the parameter to print (e.g., "Id", "Vgs", "Gm").
    """
    if mosfet_name in mosfets:
        mosfet_obj = mosfets[mosfet_name]
        if hasattr(mosfet_obj, parameter_name):
            print(mosfet_obj.Vdsat)
            parameter_value = getattr(mosfet_obj, parameter_name)
            print(f"MOSFET: {mosfet_name}, {parameter_name}: {parameter_value}")
        else:
            print(f"MOSFET: {mosfet_name} does not have parameter: {parameter_name}")
    else:
        print(f"No MOSFET found with name: {mosfet_name}")



# Construct the path
script_dir = os.path.dirname(__file__) # Directory of the current script
parent_dir = os.path.abspath(os.path.join(script_dir, "..")) # Go up one level
file_path = os.path.join(parent_dir, "test_foldedCascode.asc")

# LTC = SimCommander(file_path)  # ".." goes up one level

# data = LTSpiceLogReader(parent_dir + "\\test_foldedCascode.log") 


# Example usage:
log_file_path = parent_dir + "\\test_foldedCascode.log"  # Replace with your log file path
mosfets = parse_mosfet_data(log_file_path)


print_mosfet_parameter_by_name(mosfets, "m:x1:17", "Id")
# if mosfets:
#     for mosfet_name, mosfet_obmosfets, "fets, "n mosfets.items():
#         print(f"MOSFET: {mosfet_name}")
#         print(f"  Model: {mosfet_obj.model}")
#         print(f"  Id: {mosfet_obj.Id}")
#         print(f"  Vgs: {mosfet_obj.Vgs}")
#         print(f"  Vdsat: {mosfet_obj.Vdsat}")
#         print(f"  Vth: {mosfet_obj.Vth}")
#         print(f"  Gm: {mosfet_obj.Gm}")
#         print(f"  Gds: {mosfet_obj.Gds}")
#         # Print other parameters as needed
#         print("-" * 20)
# else:
#     print("No MOSFET data parsed.")