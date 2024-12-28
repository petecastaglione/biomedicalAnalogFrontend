import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
from siUnits import *

def gradientDescent(x, y, param, W, L, alpha, costFunctionError = None, num_iters = None):
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
    if costFunctionError is None and num_iters is None:
        raise ValueError("You must provide either a tolerance/ maximum admissable costFunctionError or a number of iterations.")

    # if num_iters is None:
    #     num_iters = 10000


    m = len(x)  # number of data points;    nr of VG values

    # Create a copy of param to avoid changing the original array
    # param = param.copy()

    # cost_history = []  # Use a list to save cost in every iteration

    def ekv_3param(VG, *params, W, L):
        Is, Vth0, kappa, = params
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

    # for j in range(num_iters):
    j = 0
    while True:
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
        # cost_history.append(cost)

        if costFunctionError is not None:
            if cost < costFunctionError:
                print(f"Maximum cost reached at iteration {j}. Cost = {num2SiStringRounded(cost)}")
                break

        if num_iters is not None:
            if j == num_iters:
                print(f"Maximum iterations reached. Cost = {num2SiStringRounded(cost)}")
                break

        # Print cost every 100 iterations
        if j % 50 == 0:
            print(f"Iteration {j}. Cost = {num2SiStringRounded(cost)}")
        j += 1


    return Is, Vth0, k, theta