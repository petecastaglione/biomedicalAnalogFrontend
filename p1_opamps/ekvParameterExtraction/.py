from PyLTSpice import *
from scipy.stats import norm
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from siUnits import *
from mosAreaCalc import getMosValueString
import os

def runSimulation(ascFilePath, simOutputPath, outputFileName):
    # r"" for raw string
    simPath = r"C:\Users\maurovlachus\AppData\Local\Programs\ADI\LTspice\LTspice.exe"
    runner = SimRunner(output_folder = simOutputPath, simulator = simPath)    

    # add mosfet models to asc file manunally
    # ascObj.add_instruction(".model N_130n nmos *+ binflag = 0 + mobmod = 1 + capmod = 2 + nqsmod = 0 + vth0 = 0.332 + nch = 5.6000000e+17 + nlx = 3.5500000e-07 + k1 = 0.3661500 + k2 = 0.00 + k3 = 0.00 + k3b = 0.00 + w0 = 0.00 + dvt0w = 0.00 + dvt1w = 0.00 + dvt2w = 0.00 + dvt0 = 8.7500000 + dvt1 = 0.7000000 + dvt2 = 5.0000000e-02 + eta0 = 4.0000000e-02 + etab = 0.00 + dsub = 0.5200000 + ua = -1.8000000e-09 + ub = 2.2000000e-18 + uc = -2.9999999e-11 + a0 = 2.1199999 + ags = -0.1000000 + b0 = 0.00 + b1 = 0.00 + keta = 4.0000000e-02 + voff = -7.9800000e-02 + vsat = 1.3500000e+05 + a1 = 0.00 + a2 = 0.9900000 + rdsw = 200 + prwg = 0.00 + prwb = 0.00 + wr = 1.0000000 + nfactor = 1.1000000 + cit = 0.00 + cdsc = 0.00 + cdscd = 0.00 + cdscb = 0.00 + pclm = 0.1000000 + pdiblc1 = 1.2000000e-02 + pdiblc2 = 7.5000000e-03 + pdiblcb = -1.3500000e-02 + drout = 0.2800000 + pscbe1 = 8.6600000e+08 + pscbe2 = 1.0000000e-20 + pvag = -0.2800000 + alpha0 = 0.00 + beta0 = 30.0000000 + ckappa = 0.8912 + cf = 1.113e-10 + clc = 5.475e-08 + cle = 6.46 + cgsl = 1.1155e-10 + cgdl = 1.1155e-10 + wint = { (0.00-(0/2)) } + wln = 0.00 + ww = 0.00 + wl = 0.00 + wwn = 1.0000000 + wwl = 0.00 + dwg = 0.00 + dwb = 0.00 + lint = { (2.5e-08-(0/2)) } + ll = 0.00 + lln = 1.0000000 + lw = 0.00 + lwn = 0.00 + lwl = 0.00 + dlc = 2e-08 + dwc = 0 + kt1 = -0.3400000 + kt1l = 4.0000000e-09 + kt2 = -5.2700000e-02 + ute = -1.2300000 + ua1 = -8.6300000e-10 + ub1 = 2.0000001e-18 + uc1 = 0.00 + at = 0.00 + prt = 0.00 + xti = 3.0 + lmin = 1.3e-7 + lmax = 1.3e-7 + wmin = 1.3e-7 + wmax = 1.0e-4 + binunit = 2 + elm = 5 + xpart = 1 + level = 7 + js = 2.50e-08 + jsw = 4.00e-13 + n = 1.0 + cj = 0.0015 + cjsw = 2e-10 + mj = 0.7175511 + mjsw = 0.3706993 + pb = 1.24859 + pbsw = 0.7731149 + rd = 0 + rs = 0 + xj = 4.5000000e-08 + ngate = 5.0000000e+20 + tox = 3.3e-09 + cgbo = 0.0e+00 + cgdo = 2.75e-10 + cgso = 2.75e-10 *+ kp = { ((3.453e-11*1.3400000e-02)/3.3e-09) } + delta = 1.0100000e-02 + u0 = 1.3400000e-02")
    # ascObj.add_instruction(".model P_130n pmos *+ binflag = 0 + mobmod = 1 + capmod = 2 + nqsmod = 0 + vth0 = -0.3499 + nch = 6.8500000e+18 + nlx = 1.6500000e-07 + k1 = 0.4087000 + k2 = 0.00 + k3 = 0.00 + k3b = 0.00 + w0 = 0.00 + dvt0w = 0.00 + dvt1w = 0.00 + dvt2w = 0.00 + dvt0 = 5.0000000 + dvt1 = 0.2600000 + dvt2 = -1.0000000e-02 + eta0 = 80.0000000 + etab = 0.00 + dsub = 1.8500000 + ua = -1.4000000e-09 + ub = 1.9499999e-18 + uc = -2.9999999e-11 + a0 = 2.1199999 + ags = 0.1000000 + b0 = 0.00 + b1 = 0.00 + keta = 3.0300001e-02 + voff = -9.10000000e-02 + vsat = 1.0500000e+05 + a1 = 0.00 + a2 = 0.4000000 + rdsw = 400 + prwg = 0.00 + prwb = 0.00 + wr = 1.0000000 + nfactor = 0.1250000 + cit = 2.7999999e-03 + cdsc = 0.00 + cdscd = 0.00 + cdscb = 0.00 + pclm = 2.5000000 + pdiblc1 = 4.8000000e-02 + pdiblc2 = 5.0000000e-05 + pdiblcb = 0.1432509 + drout = 9.0000000e-02 + pscbe1 = 1.0000000e-20 + pscbe2 = 1.0000000e-20 + pvag = -6.0000000e-02 + alpha0 = 0.00 + beta0 = 30.0000000 + ckappa = 0.8912 + cf = 1.113e-10 + clc = 5.475e-08 + cle = 6.46 + cgsl = 1.1155e-10 + cgdl = 1.1155e-10 + wint = { (0.00-(0/2)) } + wln = 0.00 + ww = 0.00 + wl = 0.00 + wwn = 0.00 + wwl = 0.00 + dwg = 0.00 + dwb = 0.00 + lint = { (2.e-08-(0/2)) } + ll = 0.00 + lln = 0.00 + lw = 0.00 + lwn = 0.00 + lwl = 0.00 + dlc = 2e-08 + dwc = 0 + kt1 = -0.3400000 + kt1l = 4.0000000e-09 + kt2 = -5.2700000e-02 + ute = -1.2300000 + ua1 = -8.6300000e-10 + ub1 = 2.0000001e-18 + uc1 = 0.00 + at = 0.00 + prt = 0.00 + xti = 3.0 + lmin = 1.3e-7 + lmax = 1.3e-7 + wmin = 1.3e-7 + wmax = 1.0e-4 + binunit = 2 + elm = 5 + xpart = 1 + level = 7 + js = 2.50e-08 + jsw = 4.00e-13 + n = 1.0 + cj = 0.0015 + cjsw = 2e-10 + mj = 0.7175511 + mjsw = 0.3706993 + pb = 1.24859 + pbsw = 0.7731149 + rd = 0 + rs = 0 + xj = 4.5000000e-08 + ngate = 5.0000000e+20 + tox = 3.3e-09 + cgbo = 0.0e+00 + cgdo = 2.75e-10 + cgso = 2.75e-10 *+ kp = { ((3.453e-11*5.2000000e-03)/3.3e-09) } + delta = 1.0100000e-02 + u0 = 5.2000000e-03")
    netlist = runner.create_netlist(ascFilePath)
    runner.run(netlist, run_filename=outputFileName)
    runner.wait_completion()

    # return raw

def hybrid_spaced_list(start, stop, num_total, mean, std_dev, truncate_start, truncate_stop):
    """
    Generates a list of points using direct mapping (ppf) and linear spacing.

    Args:
        start: The overall starting value.
        stop: The overall stopping value.
        num_total: The desired total number of points.
        mean: The mean of the normal distribution for ppf.
        std_dev: The standard deviation of the normal distribution for ppf.
        truncate_start: The start of the truncation range.
        truncate_stop: The end of the truncation range.

    Returns:
        A NumPy array containing the spaced values.
        Raises ValueError if inputs are invalid.
    """

    if start >= stop or truncate_start >= truncate_stop or truncate_start < start or truncate_stop > stop:
        raise ValueError("Invalid input values.")

    # Generate points using ppf
    cdf_values = np.linspace(0, 1, num_total)  # Oversample to have enough points after truncation
    ppf_values = norm.ppf(cdf_values, loc=mean, scale=std_dev)

    # Truncate the ppf values
    truncated_values = ppf_values[(ppf_values >= truncate_start) & (ppf_values <= truncate_stop)]

    # Calculate remaining points needed
    remaining_points = num_total - len(truncated_values)

    if remaining_points > 0:
        # Generate linspace points for the remaining intervals
        # before_linspace = np.linspace(start, truncate_start, int(remaining_points/2) + remaining_points%2, endpoint = False)
        # after_linspace = np.linspace(truncate_stop, stop, int(remaining_points/2), endpoint = True)
        # have more points in the saturation region than in super subthreshold(mosfet is essentiially turned off)
        before_linspace = np.linspace(start, truncate_start, int(remaining_points/10), endpoint = False)
        after_linspace = np.linspace(truncate_stop, stop, int(9*remaining_points/10), endpoint = True)


        # Combine the lists
        spaced_values = np.concatenate((before_linspace, truncated_values, after_linspace))
    else:
        spaced_values = truncated_values[:num_total] #If we have more points than needed, only keep the first num_total points.
    spaced_values.sort()
    return spaced_values

def prepareDCSweepSimulation(ascFilePath, parent_dir, sweeptype="linear", start=0, stop=3.3, nrPoints=1000):
    """
    Prepares a DC sweep simulation based on the specified sweep type.

    Args:
        ascFilePath: Path to the original .asc file.
        parent_dir: Directory to save the edited .asc file.
        sweeptype: "linear" or "logarithmic".
        start: Start value for the sweep (only used for linear sweep).
        stop: Stop value for the sweep.
        nrPoints: Number of points in the sweep.

    Returns:
        Path to the edited .asc file.
    """

    ascObj = AscEditor(ascFilePath)
    ascObj.set_component_value("M1", getMosValueString("N", w=siString2Num("2u"), l=siString2Num("1u")))

    if sweeptype.lower() == "linear":
        ascObj.add_instruction(f".dc V1 {start} {stop} {(stop - start) / nrPoints}")
    elif sweeptype.lower() == "logarithmic":
        if stop <= 0:
            raise ValueError("Stop value must be greater than 0 for logarithmic sweep.")
        logList = np.logspace(start, np.log10(stop), nrPoints)
        strLogList = " ".join([str(x) for x in logList])
        ascObj.add_instruction(f".dc V1 list {strLogList}")
    elif sweeptype.lower() == "hybrid":
        if stop <= 0:
            raise ValueError("Stop value must be greater than 0 for hybrid sweep.")
        # distribution mean is 0.55, stdev is 0.45, and the vgs voltages should follow the binomial(or ppf values i guess idk) between 0.1 and 1, outside values will be linearly spaced
        hybridSpacedList = hybrid_spaced_list(start, stop, nrPoints, 0.3, 0.4, 0.1, 1)
        strhybridSpacedList = " ".join([str(x) for x in hybridSpacedList])
        ascObj.add_instruction(f".dc V1 list {strhybridSpacedList}")
    else:
        raise ValueError(f"Invalid sweeptype: {sweeptype}. Must be 'linear' or 'logarithmic'.")

    ascEditedFile = os.path.join(parent_dir, "ekvParameterExtractionEdited.asc")
    ascObj.save_netlist(ascEditedFile)
    print(f"M1 value check: {ascObj.get_component_value('M1')}")
    return ascEditedFile


def generate_normal_density_points(start=0.01, end=3.3, num_points=100, mu=0.55, sigma=0.45):
    # Generate more points than needed and filter
    x = np.linspace(start, end, num_points * 3)
    
    # Calculate probability density for each point
    density = np.exp(-((x - mu) ** 2) / (2 * sigma ** 2))
    
    # Normalize density to sum to num_points
    density = density / density.sum() * num_points
    
    # Randomly select points based on density
    selected = np.random.binomial(1, density / max(density), len(x))
    points = x[selected == 1]
    
    # Ensure we have exactly num_points
    if len(points) > num_points:
        points = np.random.choice(points, num_points, replace=False)
    
    return np.sort(points)



def gradientDescent(x, y, param, W, L, alpha, num_iters):
    """
    Performs gradient descent to learn `param`. Updates param by taking `num_iters`
    gradient steps with learning rate `alpha`.

    TODO: instead of using a fixed number of iterations, implement a convergence criterion based on the cost function

    update param params using the following formula:
        param(x,j) = param(j) - alpha(j) * derivative of the cost function with respect to param(j)
        param(x,j) = param(j) - alpha(j) * dJ(param) / dtheta(j)

        j = 0, 1, 2 = Is, VTh0, kappa
        

    Parameters
    ----------
    x : array
        The input data set of shape (m), where m is the number of examples
    y : array
        The values of the function at each data point. This is a vector of shape (m, ).
    param : array
        # The parameters of the model, including the bias term. This is a vector of shape (n+1, ).
        The parameters of the model This is a vector of shape (n, ).
        [Is, VTh0, kappa]
    alpha : float
        The learning rate.
    num_iters : int
        The number of iterations to run the gradient ascent algorithm.

    Returns
    -------
    param : array
        The learned linear regression parameters.
    cost_history : list
        A list of all the cost values computed during the optimization, which can be used to plot the learning curve.
    """
    m = len(x)  # number of data points;    nr of VG values

    # Create a copy of param to avoid changing the original array
    param = param.copy()

    cost_history = []  # Use a list to save cost in every iteration

    def ekv_3param(VG, *params, W, L):
        Is, Vth0, kappa = params
        return Is*(W/L)(np.log(1 + np.exp(kappa * (VG - Vth0) / (2 * 0.0258))))**2
    
    def ekv_4param(VG, *params, W, L):
        Is, Vth0, kappa, theta = params
        return Is*(W/L)/(1+theta*kappa*(VG-Vth0))*(np.log(1 + np.exp(kappa * (VG - Vth0) / (2 * 0.0258)))**2)

    ekv = ekv_4param

    def lossFunction(x, *params, y):
        """
        Compute the loss function for gradient descent.
        
        Parameters
        ----------
        x : float
            The input data VG value
        param : array
        The parameters of the ekv model we want to fit to the data. This is a vector of shape (3, )
        param should be given in the form of [Is, VTh0, kappa]
        y : float
            The datapoints from the simulator. Drain current values for VG. This is a vector of shape (m, ).
        """
        return ekv(x, *params, W=W, L=L) - y
    
    # def exp(K, VG, VTH0):
    #     return np.exp(K * (VG - VTH0) / (2 * 0.0258))
    
    # def dekv_dIs(VG, W, L, k, Vth0, kappa, theta):
    #     return (W/L)/(1+theta*kappa*(VG-Vth0))*np.log(1 + exp(k, VG, Vth0))**2
    
    # def dekv_dk(VG, W, L, k, Vth0):
    #     return (W/L)*Is*(VG - Vth0)*exp(k, VG, Vth0)*np.log(1 + exp(k, VG, Vth0))/(0.0258*(1 + exp(k, VG, Vth0)))
    
    # def dekv_dVth0(VG, W, L, k, Vth0):
    #     return -(W/L)*Is*k*exp(k, VG, Vth0)*np.log(1 + exp(k, VG, Vth0))/(0.0258*(1 + exp(k, VG, Vth0)))
    
    # Define symbolic variables with _sym suffix
    Is_sym, W_sym, L_sym, Vth0_sym, k_sym, theta_sym, VG_sym, VT_sym = sp.symbols('Is_sym W_sym L_sym Vth0_sym k_sym theta_sym VG_sym VT_sym')
    # Symbolic EKV expression
    Id_ekv_4param_sym = Is_sym * (W_sym / L_sym) * (1 / (1 + theta_sym * k_sym * (VG_sym - Vth0_sym))) * (sp.log(1 + sp.exp(k_sym * (VG_sym - Vth0_sym) / (2 * VT_sym))))**2
    # Symbolic derivatives
    dekv_dIs_sym = sp.diff(Id_ekv_4param_sym, Is_sym)
    dekv_dk_sym = sp.diff(Id_ekv_4param_sym, k_sym)
    dekv_dVth0_sym = sp.diff(Id_ekv_4param_sym, Vth0_sym)
    dekv_dtheta_sym = sp.diff(Id_ekv_4param_sym, theta_sym)
    # Lambdify the derivatives (using the _sym variables)
    dekv_dIs = sp.lambdify((VG_sym, W_sym, L_sym, VT_sym, Is_sym, Vth0_sym, k_sym, theta_sym), dekv_dIs_sym, 'numpy')
    dekv_dk = sp.lambdify((VG_sym, W_sym, L_sym, VT_sym, Is_sym, Vth0_sym, k_sym, theta_sym), dekv_dk_sym, 'numpy')
    dekv_dVth0 = sp.lambdify((VG_sym, W_sym, L_sym, VT_sym, Is_sym, Vth0_sym, k_sym, theta_sym), dekv_dVth0_sym, 'numpy')
    dekv_dtheta = sp.lambdify((VG_sym, W_sym, L_sym, VT_sym, Is_sym, Vth0_sym, k_sym, theta_sym), dekv_dtheta_sym, 'numpy')



    # !!!!!!!!!! VERY IMPORTANT !!!!!!!!!!
    # always make sure to reassign numerical values to the parameters, 
    # so as to not call python functions with sympy symbols

    Is = param[0]
    Vth0 = param[1]
    k = param[2]
    theta = param[3]
    VT = 0.0258
    alpha_Is = alpha[0]
    alpha_Vth0 = alpha[1]
    alpha_k = alpha[2]
    alpha_theta = alpha[3]

    #interactive mode
    plt.ion()
    fig, ax = plt.subplots()
    ax.set_xlim(0, 3.3)
    ax.set_ylim(0, siString2Num("350u"))
    ax.set_xlabel("VG Values")
    ax.set_ylabel("Drain Current")
    ax.set_title("Real-time Plotting of  Gradient Descent")
    spiceOutput, = ax.plot(x, y, 'r--', label="Spice Output") #plot the output values from the LTSpice simulation
    ax.legend()
    line = None  # Initialize line outside the loop

    for j in range(num_iters):
        # Compute the cost function derivative and update each param parameter for every input data point (VG value)
        # x[j] is the current VG value
        # y[j] is the current drain current value for VG
        # L is the loss function for the current VG value
        # exp is the exponential part of the EKV model for the current VG value
        # param[0] is the current Is value
        # param[1] is the current VTh0 value
        # param[2] is the current kappa
        # for j in range(len(x)):
            
        
        # VG = x[i]

         # Plot the current approximation of the mos drain current using the current param values
        if line:
            line.remove()  # Remove the previous line
                                # *[Is, Vth0, k, theta] unpacks the list before passing it to the function, so it's equivalent to ekv(i, Is, Vth0, k, theta) and
                                # it won't generate the ValueError: not enough values to unpack (expected 4, got 1) 
        line, = ax.plot(x, [ekv(i, *[Is, Vth0, k, theta], W=W, L=L) for i in x], label=f"Iteration {j}")    
        ax.legend()

        fig.canvas.draw()
        fig.canvas.flush_events()
        # plt.pause(10e-3)  # Pause for longer to see each line


        Is = Is - alpha_Is * (2 / m) * np.sum([lossFunction(x[i], *[Is, Vth0, k, theta], y=y[i])*dekv_dIs(x[i], W, L, VT, Is, Vth0, k, theta) for i in range(len(x))])
        k = k - alpha_k * (2 / m) * np.sum([lossFunction(x[i], *[Is, Vth0, k, theta], y=y[i])*dekv_dk(x[i], W, L, VT, Is, Vth0, k, theta) for i in range(len(x))])
        Vth0 = Vth0 - alpha_Vth0 * (2 / m) * np.sum([lossFunction(x[i], *[Is, Vth0, k, theta], y=y[i])*dekv_dVth0(x[i], W, L, VT, Is, Vth0, k, theta) for i in range(len(x))])
        theta = theta - alpha_theta * (2 / m) * np.sum([lossFunction(x[i], *[Is, Vth0, k, theta], y=y[i])*dekv_dtheta(x[i], W, L, VT, Is, Vth0, k, theta) for i in range(len(x))])
                                                                         
        # param[0] = Is
        # param[1] = Vth0
        # param[2] = k

        # Compute the cost function
        cost = (1/m)*np.sum([lossFunction(x[i], *[Is, Vth0, k, theta], y=y[i])**2 for i in range(len(x))])
        cost_history.append(cost)

        # Print cost every 100 iterations
        if j % 50 == 0:
            print(f"Iteration {j}. Cost = {num2SiStringRounded(cost)}")


    return Is, Vth0, k, theta