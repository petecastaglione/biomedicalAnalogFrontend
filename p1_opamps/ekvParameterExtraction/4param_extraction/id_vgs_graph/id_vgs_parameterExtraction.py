# from pyltspice.ltspicebatch import simcommander
from PyLTSpice import *
import matplotlib.pyplot as plt         # use matplotlib for plotting the results
import scipy.optimize as optimize
from scipy.optimize import minimize
from time import sleep
import os
import sys
sys.path.append(f"C:\\Users\\maurovlachus\\OneDrive - Technical University of Cluj-Napoca\\utcn\\master\\caa\\proiect\\p1_opamps\\ekvParameterExtraction\\ekvExtractionScripts")
from ekvfitFile import *
from gradientDescent_EKV import *
from ltspiceDatapointsExtraction import *

# Construct the path
script_dir = os.path.dirname(__file__) # Directory of the current script
# print(script_dir + "\\ltspice\\lambdaExtraction.asc")
ascFilePath = script_dir + "\\ltspice\\ekvParameterExtraction.asc"
simOutputPath = script_dir + "\\ltspice"



mosType = "nmos"
nrPoints = 100

# ascObj = AscEditor(ascFilePath)
# ascObj.set_component_value("M1", getMosValueString("N", w=siString2Num("2u"), l=siString2Num("1u")))
# ascObj.save_netlist(ascFilePath)    # last edited
# ascEditedFile = prepareDCSweepSimulation(ascObj, simOutputPath, sweptSource="V1", sweeptype="hybrid", start=8e-2, stop=2.2, nrPoints=nrPoints)
# sleep(0.1)                    # create_netlist() called from runSimulation() doesn't see the edited asc file 
# runSimulation(ascEditedFile, simOutputPath, f"ekvParameterExtractionEdited_{mosType}_{nrPoints}.net")
# sleep(0.1)                   # wait for the simulation to finish before trying to read the raw file; RawRead doenst see the raw file
raw = RawRead(os.path.join(simOutputPath, f"ekvParameterExtractionEdited_{mosType}_{nrPoints}.raw"))

vdd = raw.get_trace("V1")       # result is a trace object
# # vdd = raw.get_axis()          #can print directly, as the result is a list
# # print(vdd.get_wave()) 

Isat_nmos = raw.get_trace("Id(M1)")


xdata = vdd.get_wave()
ydata = Isat_nmos.get_wave()

initialGuess = Is, VT, kappa = ekvfit(xdata, ydata, 5e-4, plotting="off")

#Is: 6.895924855941374e-07, VT: 0.3870897168702456, kappa: 0.8228179296212882
print(f"bminch variant: Is: {Is}, VT: {VT}, kappa: {kappa}")

# Example usage:
# VG = [0.1, 0.2, 0.3, 0.4, 0.5]  # Gate voltages
# ISAT = [1e-6, 2e-6, 5e-6, 10e-6, 20e-6]  # Corresponding drain currents

# is_fit, vt_fit, kappa_fit = fit_ekv_model(xdata, ydata, intitialGuess)
# print(f"Fitted parameters: Is = {Is}, VT = {VT}, kappa = {kappa}")



# print(generate_normal_density_points())
# print(hybrid_spaced_list(0.01, 3.3, 100, 0.55, 0.45, 0.1, 1))

# print(f"dc V1 list {" ".join([str(x) for x in logList])}")

# plt.plot(np.arange(len(logList)), logList)
# print(np.logspace(-6, np.log10(3.3), 1000))

# ekv_id = Is * (np.log(1 + np.exp(kappa * (xdata - VT) / (2 * 0.0258)))**2)


# print(xdata)

# ekv_id = [ekv_model(x, Is, VT, kappa) for x in xdata]
# # ekv_id = [ekv_model(x, siString2Num("400n"), 0.2, 0.815) for x in xdata]
# # ekv_id = [ekv_model(x, is_fit, vt_fit, kappa_fit) for x in xdata]


# print(num2SiStringRounded(ydata[98]))
# plt.plot(xdata, ydata, ".")
# # plt.plot(xdata, ekv_id)
# plt.xlabel('V1')
# plt.ylabel('Id(M1)')
# plt.title('Id(M1) vs VGS')
# # plt.yscale('log')
# plt.grid(True)
# plt.show()  # Add this line to display the plot



Is, Vth0, k, theta = gradientDescent(xdata, ydata, initialGuess + [0], siString2Num("2u"), siString2Num("1u"), [50e-7, 500e-2, 500e-2, 500e-2], num_iters=1000)
# Is, Vth0, k, theta = gradientDescent(xdata, ydata, initialGuess + [1], siString2Num("2u"), siString2Num("1u"), [50e-9, 500e-3, 500e-3, 500e-3], num_iters=400)
    #  learning rates: [5e-10, 5e-3, 5e-3]
# Is, Vth0, k, theta = gradientDescent(xdata, ydata, [100e-9, 0.1, 1, 0.1], siString2Num("2u"), siString2Num("1u"), [50e-9, 500e-3, 500e-3], num_iters=400)

# Is, Vth0, k, theta = gradientDescent(xdata, ydata, [1e-3, 1e-3, 1e-3, 1e-3], siString2Num("2u"), siString2Num("1u"), [50e-3, 10, 10, 10], num_iters=1000)

print(f"gradient descent variant: Is: {Is}, VT: {Vth0}, kappa: {k}, theta: {theta}")

# Is: 5.369209384184435e-07, VT: 0.3870907281865538, kappa: 0.8228162826292686, theta: 1.0000005059260586
# cost error: 3.6096814846936554e-11