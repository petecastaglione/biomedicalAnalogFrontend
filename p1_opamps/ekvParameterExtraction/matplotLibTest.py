import matplotlib.pyplot as plt
import numpy as np
import time
import os
from PyLTSpice import *

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
ekv_id = [ekv_4param(x, siString2Num("528n"), 0.38, 0.82, 1) for x in xdata]


#interactive mode
plt.ion()
fig, ax = plt.subplots()
ax.set_xlim(0, 10)
ax.set_ylim(-20, 20)
ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")
ax.set_title("Real-time Plotting with Changing Slopes and Fixed Square")

ax.legend()
line = None  # Initialize line outside the loop

for i in range(5):  # Plot 5 different lines
    slope = np.random.uniform(-2, 2)  # Random slope between -2 and 2
    intercept = np.random.randint(-10, 10)  # Random intercept
    y = slope * x + intercept  # Calculate y-values based on the new slope

    if line:
        line.remove()  # Remove the previous line
    line, = ax.plot(x, y, label=f"Line {i+1}")
    ax.legend()

    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(1)  # Pause for longer to see each line

plt.ioff()
plt.show()