# from pyltspice.ltspicebatch import simcommander
from PyLTSpice import *
from PyLTSpice.log.ltsteps import LTSpiceLogReader
from errorLogParser import *
import inspect
import re
import numpy as np
import os
from cmpTxtFiles import *
from mosAreaCalc import getMosValueString
import matplotlib.pyplot as plt         # use matplotlib for plotting the results

def runSimulation(ascFilePath, simOutputPath, outputFileName):
    # r"" for raw string
    simPath = r"C:\Users\maurovlachus\AppData\Local\Programs\ADI\LTspice\LTspice.exe"
    runner = SimRunner(output_folder = simOutputPath, simulator = simPath)    

    # add mosfet models to asc file manunally
    # ascObj.add_instruction(".model N_130n nmos *+ binflag = 0 + mobmod = 1 + capmod = 2 + nqsmod = 0 + vth0 = 0.332 + nch = 5.6000000e+17 + nlx = 3.5500000e-07 + k1 = 0.3661500 + k2 = 0.00 + k3 = 0.00 + k3b = 0.00 + w0 = 0.00 + dvt0w = 0.00 + dvt1w = 0.00 + dvt2w = 0.00 + dvt0 = 8.7500000 + dvt1 = 0.7000000 + dvt2 = 5.0000000e-02 + eta0 = 4.0000000e-02 + etab = 0.00 + dsub = 0.5200000 + ua = -1.8000000e-09 + ub = 2.2000000e-18 + uc = -2.9999999e-11 + a0 = 2.1199999 + ags = -0.1000000 + b0 = 0.00 + b1 = 0.00 + keta = 4.0000000e-02 + voff = -7.9800000e-02 + vsat = 1.3500000e+05 + a1 = 0.00 + a2 = 0.9900000 + rdsw = 200 + prwg = 0.00 + prwb = 0.00 + wr = 1.0000000 + nfactor = 1.1000000 + cit = 0.00 + cdsc = 0.00 + cdscd = 0.00 + cdscb = 0.00 + pclm = 0.1000000 + pdiblc1 = 1.2000000e-02 + pdiblc2 = 7.5000000e-03 + pdiblcb = -1.3500000e-02 + drout = 0.2800000 + pscbe1 = 8.6600000e+08 + pscbe2 = 1.0000000e-20 + pvag = -0.2800000 + alpha0 = 0.00 + beta0 = 30.0000000 + ckappa = 0.8912 + cf = 1.113e-10 + clc = 5.475e-08 + cle = 6.46 + cgsl = 1.1155e-10 + cgdl = 1.1155e-10 + wint = { (0.00-(0/2)) } + wln = 0.00 + ww = 0.00 + wl = 0.00 + wwn = 1.0000000 + wwl = 0.00 + dwg = 0.00 + dwb = 0.00 + lint = { (2.5e-08-(0/2)) } + ll = 0.00 + lln = 1.0000000 + lw = 0.00 + lwn = 0.00 + lwl = 0.00 + dlc = 2e-08 + dwc = 0 + kt1 = -0.3400000 + kt1l = 4.0000000e-09 + kt2 = -5.2700000e-02 + ute = -1.2300000 + ua1 = -8.6300000e-10 + ub1 = 2.0000001e-18 + uc1 = 0.00 + at = 0.00 + prt = 0.00 + xti = 3.0 + lmin = 1.3e-7 + lmax = 1.3e-7 + wmin = 1.3e-7 + wmax = 1.0e-4 + binunit = 2 + elm = 5 + xpart = 1 + level = 7 + js = 2.50e-08 + jsw = 4.00e-13 + n = 1.0 + cj = 0.0015 + cjsw = 2e-10 + mj = 0.7175511 + mjsw = 0.3706993 + pb = 1.24859 + pbsw = 0.7731149 + rd = 0 + rs = 0 + xj = 4.5000000e-08 + ngate = 5.0000000e+20 + tox = 3.3e-09 + cgbo = 0.0e+00 + cgdo = 2.75e-10 + cgso = 2.75e-10 *+ kp = { ((3.453e-11*1.3400000e-02)/3.3e-09) } + delta = 1.0100000e-02 + u0 = 1.3400000e-02")
    # ascObj.add_instruction(".model P_130n pmos *+ binflag = 0 + mobmod = 1 + capmod = 2 + nqsmod = 0 + vth0 = -0.3499 + nch = 6.8500000e+18 + nlx = 1.6500000e-07 + k1 = 0.4087000 + k2 = 0.00 + k3 = 0.00 + k3b = 0.00 + w0 = 0.00 + dvt0w = 0.00 + dvt1w = 0.00 + dvt2w = 0.00 + dvt0 = 5.0000000 + dvt1 = 0.2600000 + dvt2 = -1.0000000e-02 + eta0 = 80.0000000 + etab = 0.00 + dsub = 1.8500000 + ua = -1.4000000e-09 + ub = 1.9499999e-18 + uc = -2.9999999e-11 + a0 = 2.1199999 + ags = 0.1000000 + b0 = 0.00 + b1 = 0.00 + keta = 3.0300001e-02 + voff = -9.10000000e-02 + vsat = 1.0500000e+05 + a1 = 0.00 + a2 = 0.4000000 + rdsw = 400 + prwg = 0.00 + prwb = 0.00 + wr = 1.0000000 + nfactor = 0.1250000 + cit = 2.7999999e-03 + cdsc = 0.00 + cdscd = 0.00 + cdscb = 0.00 + pclm = 2.5000000 + pdiblc1 = 4.8000000e-02 + pdiblc2 = 5.0000000e-05 + pdiblcb = 0.1432509 + drout = 9.0000000e-02 + pscbe1 = 1.0000000e-20 + pscbe2 = 1.0000000e-20 + pvag = -6.0000000e-02 + alpha0 = 0.00 + beta0 = 30.0000000 + ckappa = 0.8912 + cf = 1.113e-10 + clc = 5.475e-08 + cle = 6.46 + cgsl = 1.1155e-10 + cgdl = 1.1155e-10 + wint = { (0.00-(0/2)) } + wln = 0.00 + ww = 0.00 + wl = 0.00 + wwn = 0.00 + wwl = 0.00 + dwg = 0.00 + dwb = 0.00 + lint = { (2.e-08-(0/2)) } + ll = 0.00 + lln = 0.00 + lw = 0.00 + lwn = 0.00 + lwl = 0.00 + dlc = 2e-08 + dwc = 0 + kt1 = -0.3400000 + kt1l = 4.0000000e-09 + kt2 = -5.2700000e-02 + ute = -1.2300000 + ua1 = -8.6300000e-10 + ub1 = 2.0000001e-18 + uc1 = 0.00 + at = 0.00 + prt = 0.00 + xti = 3.0 + lmin = 1.3e-7 + lmax = 1.3e-7 + wmin = 1.3e-7 + wmax = 1.0e-4 + binunit = 2 + elm = 5 + xpart = 1 + level = 7 + js = 2.50e-08 + jsw = 4.00e-13 + n = 1.0 + cj = 0.0015 + cjsw = 2e-10 + mj = 0.7175511 + mjsw = 0.3706993 + pb = 1.24859 + pbsw = 0.7731149 + rd = 0 + rs = 0 + xj = 4.5000000e-08 + ngate = 5.0000000e+20 + tox = 3.3e-09 + cgbo = 0.0e+00 + cgdo = 2.75e-10 + cgso = 2.75e-10 *+ kp = { ((3.453e-11*5.2000000e-03)/3.3e-09) } + delta = 1.0100000e-02 + u0 = 5.2000000e-03")
    netlist = runner.create_netlist(ascFilePath)
    mosType = "nmos"
    runner.run(netlist, run_filename=outputFileName)
    runner.wait_completion()

    # return raw

def runLogarithmicDCSweep(ascFilePath, simOutputPath, logList, mosType):
     # r"" for raw string
    simPath = r"C:\Users\maurovlachus\AppData\Local\Programs\ADI\LTspice\LTspice.exe"
    runner = SimRunner(output_folder = simOutputPath, simulator = simPath)    

    # add mosfet models to asc file manunally
    # ascObj.add_instruction(".model N_130n nmos *+ binflag = 0 + mobmod = 1 + capmod = 2 + nqsmod = 0 + vth0 = 0.332 + nch = 5.6000000e+17 + nlx = 3.5500000e-07 + k1 = 0.3661500 + k2 = 0.00 + k3 = 0.00 + k3b = 0.00 + w0 = 0.00 + dvt0w = 0.00 + dvt1w = 0.00 + dvt2w = 0.00 + dvt0 = 8.7500000 + dvt1 = 0.7000000 + dvt2 = 5.0000000e-02 + eta0 = 4.0000000e-02 + etab = 0.00 + dsub = 0.5200000 + ua = -1.8000000e-09 + ub = 2.2000000e-18 + uc = -2.9999999e-11 + a0 = 2.1199999 + ags = -0.1000000 + b0 = 0.00 + b1 = 0.00 + keta = 4.0000000e-02 + voff = -7.9800000e-02 + vsat = 1.3500000e+05 + a1 = 0.00 + a2 = 0.9900000 + rdsw = 200 + prwg = 0.00 + prwb = 0.00 + wr = 1.0000000 + nfactor = 1.1000000 + cit = 0.00 + cdsc = 0.00 + cdscd = 0.00 + cdscb = 0.00 + pclm = 0.1000000 + pdiblc1 = 1.2000000e-02 + pdiblc2 = 7.5000000e-03 + pdiblcb = -1.3500000e-02 + drout = 0.2800000 + pscbe1 = 8.6600000e+08 + pscbe2 = 1.0000000e-20 + pvag = -0.2800000 + alpha0 = 0.00 + beta0 = 30.0000000 + ckappa = 0.8912 + cf = 1.113e-10 + clc = 5.475e-08 + cle = 6.46 + cgsl = 1.1155e-10 + cgdl = 1.1155e-10 + wint = { (0.00-(0/2)) } + wln = 0.00 + ww = 0.00 + wl = 0.00 + wwn = 1.0000000 + wwl = 0.00 + dwg = 0.00 + dwb = 0.00 + lint = { (2.5e-08-(0/2)) } + ll = 0.00 + lln = 1.0000000 + lw = 0.00 + lwn = 0.00 + lwl = 0.00 + dlc = 2e-08 + dwc = 0 + kt1 = -0.3400000 + kt1l = 4.0000000e-09 + kt2 = -5.2700000e-02 + ute = -1.2300000 + ua1 = -8.6300000e-10 + ub1 = 2.0000001e-18 + uc1 = 0.00 + at = 0.00 + prt = 0.00 + xti = 3.0 + lmin = 1.3e-7 + lmax = 1.3e-7 + wmin = 1.3e-7 + wmax = 1.0e-4 + binunit = 2 + elm = 5 + xpart = 1 + level = 7 + js = 2.50e-08 + jsw = 4.00e-13 + n = 1.0 + cj = 0.0015 + cjsw = 2e-10 + mj = 0.7175511 + mjsw = 0.3706993 + pb = 1.24859 + pbsw = 0.7731149 + rd = 0 + rs = 0 + xj = 4.5000000e-08 + ngate = 5.0000000e+20 + tox = 3.3e-09 + cgbo = 0.0e+00 + cgdo = 2.75e-10 + cgso = 2.75e-10 *+ kp = { ((3.453e-11*1.3400000e-02)/3.3e-09) } + delta = 1.0100000e-02 + u0 = 1.3400000e-02")
    # ascObj.add_instruction(".model P_130n pmos *+ binflag = 0 + mobmod = 1 + capmod = 2 + nqsmod = 0 + vth0 = -0.3499 + nch = 6.8500000e+18 + nlx = 1.6500000e-07 + k1 = 0.4087000 + k2 = 0.00 + k3 = 0.00 + k3b = 0.00 + w0 = 0.00 + dvt0w = 0.00 + dvt1w = 0.00 + dvt2w = 0.00 + dvt0 = 5.0000000 + dvt1 = 0.2600000 + dvt2 = -1.0000000e-02 + eta0 = 80.0000000 + etab = 0.00 + dsub = 1.8500000 + ua = -1.4000000e-09 + ub = 1.9499999e-18 + uc = -2.9999999e-11 + a0 = 2.1199999 + ags = 0.1000000 + b0 = 0.00 + b1 = 0.00 + keta = 3.0300001e-02 + voff = -9.10000000e-02 + vsat = 1.0500000e+05 + a1 = 0.00 + a2 = 0.4000000 + rdsw = 400 + prwg = 0.00 + prwb = 0.00 + wr = 1.0000000 + nfactor = 0.1250000 + cit = 2.7999999e-03 + cdsc = 0.00 + cdscd = 0.00 + cdscb = 0.00 + pclm = 2.5000000 + pdiblc1 = 4.8000000e-02 + pdiblc2 = 5.0000000e-05 + pdiblcb = 0.1432509 + drout = 9.0000000e-02 + pscbe1 = 1.0000000e-20 + pscbe2 = 1.0000000e-20 + pvag = -6.0000000e-02 + alpha0 = 0.00 + beta0 = 30.0000000 + ckappa = 0.8912 + cf = 1.113e-10 + clc = 5.475e-08 + cle = 6.46 + cgsl = 1.1155e-10 + cgdl = 1.1155e-10 + wint = { (0.00-(0/2)) } + wln = 0.00 + ww = 0.00 + wl = 0.00 + wwn = 0.00 + wwl = 0.00 + dwg = 0.00 + dwb = 0.00 + lint = { (2.e-08-(0/2)) } + ll = 0.00 + lln = 0.00 + lw = 0.00 + lwn = 0.00 + lwl = 0.00 + dlc = 2e-08 + dwc = 0 + kt1 = -0.3400000 + kt1l = 4.0000000e-09 + kt2 = -5.2700000e-02 + ute = -1.2300000 + ua1 = -8.6300000e-10 + ub1 = 2.0000001e-18 + uc1 = 0.00 + at = 0.00 + prt = 0.00 + xti = 3.0 + lmin = 1.3e-7 + lmax = 1.3e-7 + wmin = 1.3e-7 + wmax = 1.0e-4 + binunit = 2 + elm = 5 + xpart = 1 + level = 7 + js = 2.50e-08 + jsw = 4.00e-13 + n = 1.0 + cj = 0.0015 + cjsw = 2e-10 + mj = 0.7175511 + mjsw = 0.3706993 + pb = 1.24859 + pbsw = 0.7731149 + rd = 0 + rs = 0 + xj = 4.5000000e-08 + ngate = 5.0000000e+20 + tox = 3.3e-09 + cgbo = 0.0e+00 + cgdo = 2.75e-10 + cgso = 2.75e-10 *+ kp = { ((3.453e-11*5.2000000e-03)/3.3e-09) } + delta = 1.0100000e-02 + u0 = 5.2000000e-03")
    ascObj = AscEditor(ascFilePath)

    strLogList = " ".join([str(x) for x in logList])
    ascObj.add_instruction(f".dc V1 list {strLogList}")
    
    netlist = runner.create_netlist(ascFilePath)
    runner.run(netlist, run_filename=f"ekvParameterExtractionEdited_{mosType}")
    runner.wait_completion()



def prepareDCSweepSimulation(ascFilePath, parent_dir, sweeptype = "linear", start = 0, stop = 3.3, nrPoints = 1000):

    ascObj = AscEditor(ascFilePath)
    ascObj.set_component_value("M1", getMosValueString("N", w=siString2Num("2u"), l=siString2Num("1u")))
    ascObj.add_instruction(f".dc V1 {start} {stop} {(stop-start)/nrPoints}")
    ascEditedFile = os.path.join(parent_dir, "ekvParameterExtractionEdited.asc")
    ascObj.save_netlist(ascEditedFile)
    print(f"M1 value check: {ascObj.get_component_value("M1")}")
    return ascEditedFile



# Construct the path
script_dir = os.path.dirname(__file__) # Directory of the current script
parent_dir = os.path.abspath(os.path.join(script_dir, "..", "parameterExtraction")) # Go up one level
ascFilePath = os.path.join(parent_dir, "ekvParameterExtraction.asc")
simOutputPath = parent_dir


mosType = "nmos"

ascEditedFile = prepareAscFile(ascFilePath, simOutputPath)
# runDcSweep(ascEditedFile, simOutputPath)
logList = np.logspace(-6, np.log10(3.3), 1000)
runSimulation(ascEditedFile, simOutputPath, f"ekvParameterExtractionEdited_{mosType}")

runLogarithmicDCSweep(ascEditedFile, simOutputPath, logList, 1000, "nmos")

raw = RawRead(os.path.join(simOutputPath, "ekvParameterExtractionEdited_1.raw"))


# print(raw.get_trace_names())            # Get and print a list of all the traces
# print(raw.get_raw_property())           # Print all the properties found in the Header section

vdd = raw.get_trace("V1")       # result is a trace object
# vdd = raw.get_axis()          #can print directly, as the result is a list
# print(vdd.get_wave()) 

Isat_nmos = raw.get_trace("Id(M1)")


xdata = vdd.get_wave()
ydata = Isat_nmos.get_wave()
# ydata = math.log(ydata)



# print(f"dc V1 list {" ".join([str(x) for x in logList])}")

# plt.plot(np.arange(len(logList)), logList)
# print(np.logspace(-6, np.log10(3.3), 1000))

# plt.plot(xdata, ydata)
# plt.xlabel('V1')
# plt.ylabel('Id(M1)')
# plt.title('Id(M1) vs VGS')
# plt.yscale('log')
# plt.grid(True)
# plt.show()  # Add this line to display the plot



# compareTextFiles(os.path.join(parent_dir, simOutputPath, "test_foldedCascode_1.net"), os.path.join(parent_dir, "test_foldedCascode.net"))


