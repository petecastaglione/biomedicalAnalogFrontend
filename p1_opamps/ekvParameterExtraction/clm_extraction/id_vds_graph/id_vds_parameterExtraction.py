# from pyltspice.ltspicebatch import simcommander
from PyLTSpice import *
import matplotlib.pyplot as plt         # use matplotlib for plotting the results
import scipy.optimize as optimize
from scipy.optimize import minimize
from time import sleep
import os
import sys
import numpy as np
# sys.path.append(os.path.join("..", os.getcwd()))
sys.path.append(f"C:\\Users\\maurovlachus\\OneDrive - Technical University of Cluj-Napoca\\utcn\\master\\caa\\proiect\\p1_opamps\\ekvParameterExtraction\\ekvExtractionScripts")
# Now you can import linefit
from ltspiceDatapointsExtraction import *
from gradientDescent_EKV import *





# Construct the path
script_dir = os.path.dirname(__file__) # Directory of the current script
print(script_dir + "\\ltspice\\lambdaExtraction.asc")
# script_dir = os.getcwd() # Directory of the current script
# parent_dir = os.path.abspath(os.path.join(script_dir, "..", "ltpice")) # Go up one level
ascFilePath = script_dir + "\\ltspice\\lambdaExtraction.asc"
simOutputPath = script_dir + "\\ltspice"




mosType = "nmos"
nrPoints = 100

# ASC EDITING
ascObj = AscEditor(ascFilePath)
ascObj.set_component_value("M1", getMosValueString("N", w=siString2Num("2u"), l=siString2Num("1u")))
ascObj.save_netlist(ascFilePath)    # last edited

ascEditedFile = prepareDCSweepSimulation(ascObj, simOutputPath, sweptSource="V1", sweeptype="linear", start=0.8, stop=3.3, nrPoints=nrPoints)
# ascObj.set_component_value("V2", "0.8")
# ascObj.save_netlist(ascEditedFile)

V2 = [0.8, 1, 1.4]

for vg in V2:
    ascObj.set_component_value("V2", str(vg))
    ascObj.save_netlist(ascEditedFile)
    sleep(0.1)                    # create_netlist() called from runSimulation() doesn't see the edited asc file 
    runSimulation(ascEditedFile, simOutputPath, f"lambdaExtractionEdited_{mosType}_{vg}_{nrPoints}.net")
    sleep(0.1)                   # wait for the simulation to finish before trying to read the raw file; RawRead doenst see the raw file
    

# RAW FILE PARSING

ID_nmos = []
for vg in V2:
    raw = RawRead(os.path.join(simOutputPath, f"lambdaExtractionEdited_{mosType}_{vg}_{nrPoints}.raw"))
    ID_nmos.append(raw.get_trace("Id(M1)"))

vds = raw.get_trace("V1")       # result is a trace object
xdata = vds.get_wave()
# vgs = raw.get_trace("V2")       # result is a trace object

# # # vdd = raw.get_axis()          #can print directly, as the result is a list
# # # print(vdd.get_wave()) 

# print(ID_nmos[0].get_wave())
# print(ID_nmos[1].get_wave())
# print(ID_nmos[2].get_wave())





for Id, vg in zip(ID_nmos, V2):
    ydata = Id.get_wave()
    plt.plot(xdata, ydata, label = f"V2={vg}V", linewidth=2)

# print(num2SiStringRounded(ydata[98]))

# Plot all curves
# plt.plot(xdata, ID_nmos[0].get_wave(), 'b-', label="V2=0.8V", linewidth=2)
# plt.plot(xdata, ID_nmos[1].get_wave(), 'r--', label="V2=1.0V", linewidth=2)
# plt.plot(xdata, ID_nmos[2].get_wave(), 'g-.', label="V2=1.4V", linewidth=2)

# plt.plot(xdata, ekv_id)
plt.xlabel('VDS')
plt.ylabel('Id(M1)')
plt.title('Id(M1) vs VDS')
# plt.yscale('log')
plt.grid(True)
plt.show()  # Add this line to display the plot



# Is, Vth0, k, theta = gradientDescent(xdata, ydata, intitialGuess + [1e-5], siString2Num("2u"), siString2Num("1u"), [1e-15, 1e-3, 1e-3], num_iters=1000)
# Is, Vth0, k, theta = gradientDescent(xdata, ydata, initialGuess + [5], siString2Num("2u"), siString2Num("1u"), [50e-9, 500e-3, 500e-3, 500e-3], num_iters=400)
    #  learning rates: [5e-10, 5e-3, 5e-3]
# Is, Vth0, k, theta = gradientDescent(xdata, ydata, [100e-9, 0.1, 1, 0.1], siString2Num("2u"), siString2Num("1u"), [50e-9, 500e-3, 500e-3], num_iters=400)

# Is, Vth0, k, theta = gradientDescent(xdata, ydata, [1e-3, 1e-3, 1e-3, 1e-5], siString2Num("2u"), siString2Num("1u"), [50e-9, 500e-3, 500e-3, 500e-3], num_iters=1000)

# print(f"gradient descent variant: Is: {Is}, VT: {Vth0}, kappa: {k}, theta: {theta}")

# Is: 5.369209384184435e-07, VT: 0.3870907281865538, kappa: 0.8228162826292686, theta: 1.0000005059260586
# cost error: 3.6096814846936554e-11