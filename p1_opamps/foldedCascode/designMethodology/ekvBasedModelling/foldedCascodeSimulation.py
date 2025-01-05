import numpy as np
import os
import sys
import time
sys.path.append(f"C:\\Users\\maurovlachus\\OneDrive - Technical University of Cluj-Napoca\\utcn\\master\\caa\\proiect\\p1_opamps\\ekvParameterExtraction\\ekvExtractionScripts")
sys.path.append(f"C:\\Users\\maurovlachus\\OneDrive - Technical University of Cluj-Napoca\\utcn\\master\\caa\\proiect\\p1_opamps\\python")
from siUnits import *
from PyLTSpice import *
from PyLTSpice.log.ltsteps import LTSpiceLogReader
from errorLogParser import *
from ltspiceDatapointsExtraction import *
import foldedCascodeDesign as design
from ascFileMosfetValuesClearing import process_asc_file_inplace


#EKV Model parameters
W_L = 2         #W/L was 2u/1u for the reference transistors 
VT = 0.0258
#NMOS
Is_n = siString2Num("689n")
Vth0_n = siString2Num("387m")
k_n = 0.822
n_n = 1/k_n
uCox_n = (Is_n*k_n)/(2*2*VT**2)
u_n = 1.343e-2
lambdac_n = 0.04
#PMOS
Is_p = siString2Num("904.8n")
Vth0_p = siString2Num("371m")
k_p = 0.816
n_p = 1/k_p
uCox_p = (Is_p*k_p)/(2*2*VT**2)
u_p = 5.2e-3
lambdac_n = 0.02

def getDrainCurrent(gm, IC, mostype):
    if mostype == "n":
        return (gm*VT*np.sqrt(IC))/(k_n*(1-np.exp(-np.sqrt(IC))))
    elif mostype == "p":
        return (gm*VT*np.sqrt(IC))/(k_p*(1-np.exp(-np.sqrt(IC))))
    else:
        raise ValueError("Invalid mosfet type")

def getDimensions(IC, ID, mostype):
    if mostype == "n":
        return (ID)/(2*uCox_n*n_n*VT**2*IC)
    elif mostype == "p":
        return (ID)/(2*uCox_p*n_p*VT**2*IC)
    else:
        raise ValueError("mostype has to be either \"n\" or \"p\"")


# Construct the path
script_dir = os.path.dirname(__file__) # Directory of the current script
# print(script_dir + "\\ltspice\\lambdaExtraction.asc")
ascFilePath = script_dir + "\\ltspice\\nmosFoldedCascode_ekvModellingEdited.asc"
simOutputPath = script_dir + "\\ltspice"


#Modifying mosfets sizes


# for mos in design.designedMosfets:
#     print(f"{mos.name} has W={num2SiStringRounded(mos.W)} and L={num2SiStringRounded(mos.L)}")

ascObj = AscEditor(ascFilePath)

# for mos in design.designedMosfets:
#     ascObj.set_component_value(mos.name, getMosValueString(mos.type, w=mos.W, l=mos.L))

    
# ascObj.save_netlist(ascFilePath)    # last edited

# process_asc_file_inplace(ascFilePath)

filename = f"foldedCascodeEkvModelled_dcOp"

runSimulation(ascFilePath, simOutputPath, f"{filename}.net")
time.sleep(0.1)                   # wait for the simulation to finish before trying to read the raw file; RawRead doenst see the raw file





# # Example usage:
log_file_path = simOutputPath + f"\\{filename}.log"  # Replace with your log file path
mosfets = parseMosfetOPs(log_file_path)

for mos in mosfets:
    print(mos)

# print_mosfet_parameter_by_name(mosfets, "m:x1:17", "Id")
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