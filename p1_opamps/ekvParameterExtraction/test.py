import matplotlib.pyplot as plt
import numpy as np
import time
import os
from PyLTSpice import *
from siUnits import *


def ekv_4param(VG, *params, W, L):
        Is, Vth0, kappa, theta = params
        return Is*(W/L)/(1+theta*kappa*(VG-Vth0))*(np.log(1 + np.exp(kappa * (VG - Vth0) / (2 * 0.0258)))**2)


# Construct the path
script_dir = os.path.dirname(__file__) # Directory of the current script
parent_dir = os.path.abspath(os.path.join(script_dir, "..", "parameterExtraction")) # Go up one level
ascFilePath = os.path.join(parent_dir, "ekvParameterExtraction.asc")
simOutputPath = parent_dir

mosType = "nmos"
nrPoints = 100
raw = RawRead(os.path.join(simOutputPath, f"ekvParameterExtractionEdited_{mosType}_{nrPoints}.raw"))

vdd = raw.get_trace("V1")     
Isat_nmos = raw.get_trace("Id(M1)")

xdata = vdd.get_wave()
simOutput = Isat_nmos.get_wave()




# 5.279333061934613e-07, VT: 0.38700212546793505, kappa: 0.8228144696006071, theta: 1
ekv_id = [ekv_4param(x, siString2Num("528n"), 0.38, 0.82, 1, W = siString2Num("2u"), L=siString2Num("1u")) for x in xdata]


# #interactive mode
# plt.ion()
# fig, ax = plt.subplots()
# ax.set_xlim(0, 10)
# ax.set_ylim(-20, 20)
# ax.set_xlabel("X-axis")
# ax.set_ylabel("Y-axis")
# ax.set_title("Real-time Plotting with Changing Slopes and Fixed Square")

# ax.plot(xdata, simOutput, label=f"Spice output ")
# ax.plot(xdata, ekv_id, label=f"EKV output ")
# fig.canvas.draw()
# fig.canvas.flush_events()
plt.plot(xdata, simOutput)
plt.plot(xdata, ekv_id)
plt.xlabel('VG')
plt.ylabel('Id')
plt.title('Id(M1) vs VGS')
# plt.yscale('log')
plt.grid(True)
plt.show()  # Add this line to display the plot