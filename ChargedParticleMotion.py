import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import argparse

# Parse optional arguments so that the various plots asked for by the
# porfolio assignment can be made by passing "-1", "-2", ... 
#
def parse_arguments():
    parser = argparse.ArgumentParser();

    # Optional arguments
    parser.add_argument("-1", "--plotMagField", action="store_true", help="Plots the magnetic field");
    parser.add_argument("-2", "--plotPartTraj", action="store_true", help="Plots charged particle's trajectories within space");
    parser.add_argument("-3", "--plotKinEnergy", action="store_true", help="Plots charged particles kinetic energy over time")
    parser.add_argument("-4", "--plotEPartTraj", action="store_true", help="Plots charged particles trajectories with an electric field")
    parser.add_argument("-5", "--plotEKinEnergy", action="store_true", help="Plots charged particles kinetic energy with an electric field")
    args = parser.parse_args();

    return args;

# Function to calculate the magnetic field, vec_B,
# based on the position, vec_x.
def B_func(vec_x, B_0, x_0, x_c):
    x = vec_x[0];
    B_z = B_0 * x_0 / (x - x_c); # "y" is unused in this magnetic field.
    return B_z;

# Function to plot array_of_Bz at positions of x
def plot_B_func(array_of_xs, array_of_ys, array_of_Bzs):
    plt.pcolormesh(array_of_xs, array_of_ys, array_of_Bzs.T, shading = 'auto',);
    plt.xlabel(r'$\hat{x}$ (normalised to thermal hydrogen gyro-radius, $ρ_H$)');
    plt.ylabel(r'$\hat{y}$ (normalised to thermal hydrogen gyro-radius, $ρ_H$)');
    plt.title(r"Example magnetic field in the z direction, $B_z$, at various points of $\hat{x}$ and $\hat{y}$");
    plt.colorbar(label=r'$B_z$ (normalised to radial magnetic field, $B_r$)');

def df_dt(current_t, current_vec_x, B_0, x_0, x_c, vec_E, q, m):
    v_x = current_vec_x[2];
    v_y = current_vec_x[3];
    B_z = B_func(current_vec_x, B_0, x_0, x_c);
    E_x = vec_E[0];
    E_y = vec_E[1];

    dx_dt = v_x;
    dy_dt = v_y;

    dv_x_dt = q * (E_x + v_y * B_z) / m;
    dv_y_dt = q * (E_y - v_x * B_z) / m;

    return [dx_dt, dy_dt, dv_x_dt, dv_y_dt];

def solve_df_dt(from_t, until_t, num_samples, x_t0, y_t0, v_x_t0, v_y_t0, B_0, x_0, x_c, vec_E, q, m):
    # Create array of times over which to calculate.
    t = np.linspace(from_t, until_t, num_samples);

    # Set the initial conditions.
    f0 = [x_t0, y_t0, v_x_t0, v_y_t0];

    # Solve the equation dfdt.
    result = solve_ivp(
        df_dt, 
        [t[0], t[-1]], 
        f0, 
        t_eval = t, 
        args = [B_0, x_0, x_c, vec_E, q, m]
    )

    x_of_t = result.y[0,:];
    y_of_t = result.y[1,:];
    v_x_of_t = result.y[2,:];
    v_y_of_t = result.y[3,:];


    return t, x_of_t, y_of_t, v_x_of_t, v_y_of_t;

def main():
    # Parse the args to determine which sections of code to run:
    args = parse_arguments();

    # Set initial values and constants.
    # ---------------------------------

    # Create x-y values for which to calculate Bz.
    number_of_xs = 1001; # Called "nx" in the script.
    number_of_ys = 501; # Called "ny" in the script.
    max_value_of_x = 100.0; # Called "L_x" in the script.
    max_value_of_y = 50.0; # Called "L_y" in the script.
    array_of_xs = np.linspace(0, max_value_of_x, number_of_xs); # Called "xx" in the script.
    array_of_ys = np.linspace(0, max_value_of_y, number_of_ys); # Called "yy" in the script.

    # Calculate constants.
    x_0 = max_value_of_x / 2;
    x_c = -max_value_of_x;
    B_0 = 1.0;

    # Plot the magnetic field over an area within the x-y plain.
    # ----------------------------------------------------------

    if not (args.plotKinEnergy or args.plotEKinEnergy):
        # Initialise B_z array.
        array_of_B_zs = np.zeros([number_of_xs, number_of_ys]); # Called "Bmag" in the script.

        # Calculate B_z at point (x, y).
        for ix, x in enumerate(array_of_xs):
            for iy, y in enumerate(array_of_ys):
                vec_x = np.array([x, y]);
                array_of_B_zs[ix, iy] = B_func(vec_x, B_0, x_0, x_c);

        # Plot B_z at each point of x and y.
        plot_B_func(array_of_xs, array_of_ys, array_of_B_zs);

    # Plot trajectories of charged particles within the B field
    # ---------------------------------------------------------

    # Set arrays of results for each particle.
    ts = [];
    x_of_ts = [];
    y_of_ts = [];
    v_x_of_ts = [];
    v_y_of_ts = [];

    if not args.plotMagField:
        # Set arrays of initial values for each of the charged particles in the script.
        x_t0s = [3 * max_value_of_x / 4, max_value_of_x / 2, max_value_of_x / 4,
        max_value_of_x / 2];
        v_x_t0s = [1.0, 1.0, 1.0, -1.0];
        qs = [1., -1., 1., 1.];
        ms = [1., 1., .1, .1];

        # Set an electric field if relevant argument set.
        if args.plotEPartTraj or args.plotEKinEnergy:
            vec_E = [0, 0.01];
        else:
            vec_E = [0, 0];

        # Calculate the trajectories of the charged particles.
        for i in range(len(ms)):
            t, x_of_t, y_of_t, v_x_of_t, v_y_of_t = solve_df_dt(
                from_t=0,
                until_t=500,
                num_samples=10000, # Selected to compute the m=0.1 particles with sufficient resolution.
                x_t0=x_t0s[i],
                y_t0=max_value_of_y/2,
                v_x_t0=v_x_t0s[i],
                v_y_t0=0,
                x_0=x_0,
                B_0=B_0,
                x_c=x_c,
                vec_E=vec_E,
                q=qs[i],
                m=ms[i]
            );
            # Add result to results array.
            ts.append(t);
            x_of_ts.append(x_of_t);
            y_of_ts.append(y_of_t);
            v_x_of_ts.append(v_x_of_t);
            v_y_of_ts.append(v_y_of_t);

    if args.plotPartTraj or args.plotEPartTraj:
        for i in range(len(ts)):
            # Array of colours to use for the plot of each particle.
            colours = ["maroon", "red", "orange", "magenta"];

            # Plot the particle trajectories on top of the B_z plot.
            label = f"particle {i}" + ": $x_{t=0}$=" + str(x_t0s[i]) + ", $v_{x,t=0}$=" + str(v_x_t0s[i]) + f", q={qs[i]}, m={ms[i]}"
            plt.plot(x_of_ts[i], y_of_ts[i], linewidth=.5, color=colours[i], label=label);
        
        plt.title("Trajectories of charged particles within a static magnetic field in \n the z direction, $B_z$, and no electric field.");
        plt.legend();

    # Plot the kinetic energies of charged particles over time.
    # ---------------------------------------------------------

    KE_of_ts = [];

    # Calculate kinetic energy for each of the particles.
    if args.plotKinEnergy or args.plotEKinEnergy:
        plt.clf(); # Resets the plot.
        for i in range(len(ts)):
            KE_of_t = .5 * ms[i] * (v_x_of_ts[i]**2 + v_y_of_ts[i]**2);
            KE_of_ts.append(KE_of_t);

            # Plot particle energies  against time on a new plot.
            plt.plot(ts[i], KE_of_t);

    plt.show();

if __name__ == "__main__":
    main();