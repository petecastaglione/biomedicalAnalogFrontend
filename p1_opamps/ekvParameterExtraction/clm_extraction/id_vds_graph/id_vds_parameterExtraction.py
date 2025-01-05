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
# print(script_dir + "\\ltspice\\lambdaExtraction.asc")
# script_dir = os.getcwd() # Directory of the current script
# parent_dir = os.path.abspath(os.path.join(script_dir, "..", "ltpice")) # Go up one level
ascFilePath = script_dir + "\\ltspice\\lambdaExtractionEdited.asc"
simOutputPath = script_dir + "\\ltspice"




mosType = "nmos"
nrPoints = 100

# ASC EDITING
ascObj = AscEditor(ascFilePath)
ascObj.set_component_value("M2", getMosValueString("P", w=siString2Num("2u"), l=siString2Num("1u")))        #8e-8
ascObj.save_netlist(ascFilePath)    # last edited

# ascEditedFile = prepareDCSweepSimulation(ascObj, simOutputPath, sweptSource="V1", sweeptype="linear", start=0.2, stop=3.3, nrPoints=nrPoints)
# ascObj.set_component_value("V2", "0.8")
# ascObj.save_netlist(ascEditedFile)

# few values
# V2 = [0.8, 1, 1.4]
V2 = np.round(np.linspace(0.1, 0.8, 10), 2)

# multiple V2 values

# for vg in V2:
#     ascObj.set_component_value("V2", str(vg))
#     ascObj.save_netlist(ascFilePath)
#     # sleep(0.1)                    # create_netlist() called from runSimulation() doesn't see the edited asc file 
#     runSimulation(ascFilePath, simOutputPath, f"lambdaExtractionEdited_{vg}_{nrPoints}.net")
#     # sleep(0.1)                   # wait for the simulation to finish before trying to read the raw file; RawRead doenst see the raw file
    


#remove the last item in the list
# V2 = V2[:-1]

# RAW FILE PARSING

ID_nmos = []
ID_pmos = []
for vg in V2:
    raw = RawRead(os.path.join(simOutputPath, f"lambdaExtractionEdited_{vg}_{nrPoints}.raw"))
    ID_nmos.append(raw.get_trace("Id(M1)").get_wave())
    # reverse to negate the id values of the pmos
    ID_pmos.append(np.abs(raw.get_trace("Id(M2)").get_wave()))

vds = raw.get_trace("vdd")       # result is a trace object
xdata = vds.get_wave()
# vgs = raw.get_trace("V2")       # result is a trace object

# # # vdd = raw.get_axis()          #can print directly, as the result is a list
# # # print(vdd.get_wave()) 

# print(ID_nmos[0].get_wave())
# print(ID_nmos[1].get_wave())
# print(ID_nmos[2].get_wave())

# Is = siString2Num("689n")
# Vth0 = siString2Num("387m")
# k = 0.822

Is = siString2Num("727n")
Vth0 = siString2Num("400m")
k = 0.816
n = 1/k

VT = 0.0258
W_L = 2         #W/L was 2u/1u for the reference transistors 
uCox = (Is*k)/(2*2*VT**2)


def ekv(VG):
        return Is*(np.log(1 + np.exp(k * (VG - Vth0) / (2*VT))))**2


def VDSat(VG):
    return (VG - Vth0)

# for Id, vg in zip(ID_pmos, V2):
#     ydata = Id
#     plt.plot(xdata, ydata, label = f"V2={vg}V", linewidth=2)


# plt.xlabel('VDS')
# plt.ylabel('Id(M1)')
# plt.title('Id(M1) vs VDS')
# plt.yscale('log')
# plt.legend(loc='upper right')  # Explicitly set legend location
# plt.grid(True)
# plt.show()  # Add this line to display the plot


# print only for currents bigger than the current for which vg = vd (the parameters where extracted from a transistor which was diode connected)
# for Id, vg in zip(ID_nmos, V2):
#     ydata = Id.get_wave()[Id.get_wave() >= ekv(vg)]
#     print(f"vg: {vg};  {len(ydata)}")
#     # xdata = xdata[-len(ydata):]
#     print(f"vg: {vg};  {len(xdata)}")
#     plt.plot(xdata[-len(ydata):], ydata, label = f"V2={vg}V", linewidth=2)


# Plot only for values bigger than VDSat
# in weak inv, VDSat = [3*VT, 5*VT]
# for Id, vg in zip(ID_nmos, V2):
#     print(max(VDSat(vg), 3*VT))
#     # print(VDSat(vg))
#     # if VDSat(vg) >= 3*VT:
#     #     x = xdata[xdata >= VDSat(vg)]
#     # else:
#     #     x = xdata[xdata >= VDSat(VT)]
#     x = xdata[xdata >= max(VDSat(vg), 3*VT)]
#     ydata = Id.get_wave()[-len(x):]
#     plt.plot(x, ydata, label = f"V2={vg}V", linewidth=2)



# Plot only for values bigger than the ekv value for the drain current
# for Id, vg in zip(ID_nmos, V2):
#     ydata = Id.get_wave()[Id.get_wave() >= ekv(vg)]
#     x = xdata[-len(ydata):]
#     print(f"ydata len: {len(ydata)}")
#     print(f"xdata len: {len(x)}")
#     plt.plot(x, ydata, label = f"V2={vg}V", linewidth=2)

# plt.xlabel('VDS')
# plt.ylabel('Id(M1)')
# plt.title('Id(M1) vs VDS')
# plt.yscale('log')
# plt.legend(loc='upper right')  # Explicitly set legend location
# plt.grid(True)
# plt.show()  # Add this line to display the plot

# sys.exit()

# V2 = V2[V2 >= 0.4]
i = np.where(V2 >= 0.5)[0][0]
vg = V2[i]
ydata = ID_pmos[i]
# ydata = Id.get_wave()

# #use only those ID values that are in saturation
# ydata = Id.get_wave()[Id.get_wave() > ekv(vg)]
# xdata = xdata[-len(ydata):]
# # plt.plot(xdata, ydata, label = f"V2={vg}V", linewidth=2)

xdata = xdata[xdata > 0.2]
ydata = ydata[-len(xdata):]


lambdac = 0.0001

# # lambdac = gradientDescent_id_vds(xdata, ydata, lambdac, ydata[0]/(1+lambdac*xdata[0]), 1e11, num_iters = 200)

lambdac = gradientDescent_id_vds(xdata, ydata, lambdac, ydata[0]/(1+lambdac*xdata[0]), 1e10, num_iters = 50)


print(f"lambda: {lambdac}")

#weak inversion
#lambda_n: 0.0961
#lamba_p: 0.049
#moderate inversion:
#lambda_n: 0.04774
#lamba_p: 0.02
#strong inversion:
#lambda_n: 0.035511
#lamba_p: 0.015
