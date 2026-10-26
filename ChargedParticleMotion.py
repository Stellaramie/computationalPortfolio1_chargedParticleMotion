import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import argparse

# Parse optional arguments so that the various plots asked for by the
# porfolio assignment can be made.
def parse_arguments():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter);

    # Optional argument
    parser.add_argument(
        "-b",
        "--plot-magnetic-field",
        action="store_true",
        help="Plots magnetic field strength (along with particle trajectories if enabled.)"
    )
    parser.add_argument(
        "-t",
        "--plot-trajectories",
        action="store_true",
        help="Plots charged particle's trajectories within space."
    )
    parser.add_argument(
        "-k",
        "--plot-kinetic-energy",
        action="store_true",
        help="Plots charged particle's kinetic energy over time."
    )
    parser.add_argument(
        "-E",
        "--electric-field",
        help="Set the normalised electric field strength in the x and y directions",
        nargs=2,
        type=float,
        default=[0.,0.],
        metavar=('E_x','E_y')
    )

    args = parser.parse_args();

    return args;

# Function to calculate the magnetic field, vec_B, based on the position, vec_x.
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
    # =================================

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
    # ==========================================================

    if args.plot_magnetic_field:
        # Initialise B_z array.
        array_of_B_zs = np.zeros([number_of_xs, number_of_ys]); # Called "Bmag" in the script.

        # Calculate B_z at point (x, y).
        for ix, x in enumerate(array_of_xs):
            for iy, y in enumerate(array_of_ys): # Loops through each x, y coordinate
                vec_x = np.array([x, y]);
                array_of_B_zs[ix, iy] = B_func(vec_x, B_0, x_0, x_c); # Calculate the B field at each coordinate and adds to list of results

        # Plot B_z at each point of x and y.
        plot_B_func(array_of_xs, array_of_ys, array_of_B_zs);

    # Plot trajectories of charged particles within the B field
    # =========================================================

    # initialise lists of results for each particle.
    ts = [];
    x_of_ts = [];
    y_of_ts = [];
    v_x_of_ts = [];
    v_y_of_ts = [];

    # Set lists of initial values for each of the charged particles in the script.
    if args.plot_kinetic_energy or args.plot_trajectories:
        x_t0s = [3 * max_value_of_x / 4, max_value_of_x / 2, max_value_of_x / 4,
        max_value_of_x / 2];
        v_x_t0s = [1.0, 1.0, 1.0, -1.0];
        qs = [1., -1., 1., 1.];
        ms = [1., 1., .1, .1];
        colours = ["maroon", "red", "orange", "magenta"]; # List of colours to use for the plot of each particle.
        labels = []; # Generate the labels for each particle for plotting
        for i, _ in enumerate(ms):
            label = f"particle {i}" + ": $x_{t=0}$=" + str(x_t0s[i]) + ", $v_{x,t=0}$=" + str(v_x_t0s[i]) + f", q={qs[i]}, m={ms[i]}";
            labels.append(label);


        # Set an electric field if relevant argument set.
        vec_E = args.electric_field;

        # Calculate the trajectories of the charged particles.
        for i, _ in enumerate(ms): # Loops through each particle
            t, x_of_t, y_of_t, v_x_of_t, v_y_of_t = solve_df_dt(
                from_t=0,
                until_t=500,
                num_samples=10000, # Selected 10000 to compute the m=0.1 particles with sufficient resolution.
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

            # Add result to results list.
            ts.append(t);
            x_of_ts.append(x_of_t);
            y_of_ts.append(y_of_t);
            v_x_of_ts.append(v_x_of_t);
            v_y_of_ts.append(v_y_of_t);

    # Plot the particle trajectories.
    if args.plot_trajectories:
        for i, _ in enumerate(ms): # Loops through each particle
            plt.plot(x_of_ts[i], y_of_ts[i], linewidth=.5, color=colours[i], label=labels[i]);
        if args.electric_field == [0.,0.]:
            plt.title("Trajectories of charged particles within a static magnetic field in \n the z direction, $B_z$.");
        else:
            plt.title("Trajectories of charged particles within a static magnetic field in \n the z direction, $B_z$, and a static electric field in the y direction, $E_y$.")
        plt.legend()
        plt.show()
    elif args.plot_magnetic_field:
        plt.show()

    # Plot the kinetic energies of charged particles over time.
    # =========================================================

    # Initialise list containing the KE over time for each particle.
    KE_of_ts = [];

    # Calculate kinetic energy for each of the particles.
    if args.plot_kinetic_energy:
        #plt.clf(); # Resets the plot.
        for i, _ in enumerate(ms): # Loops through each particle
            KE_of_t = ms[i] * (v_x_of_ts[i]**2 + v_y_of_ts[i]**2); # Using normalised KE equation
            KE_of_ts.append(KE_of_t); # Adds KE over time for particle [i]

            # Plot each particle energy against time.
            plt.plot(ts[i], KE_of_ts[i], color=colours[i], label=labels[i]);

        # Set plot titles
        if args.electric_field == [0.,0.]:
            plt.title("Kinetic energy of charged particles within a static magnetic field in \n the z direction, $B_z$.")
        else:
            plt.title("Kinetic energy of charged particles within a static magnetic field in \n the z direction, $B_z$, and a static electric field, $E$.")
        plt.xlabel(f"Time (Normalised to gyro-period, $τ_H$)")
        plt.ylabel(r"Kinetic energy (Normalised to $0.5 \cdot m_H \cdot v_{th,H}^2$)")
        plt.grid();

        # Calculate and print the average change in KE over time
        KE_differences = np.array(KE_of_ts)[:,-1] - np.array(KE_of_ts)[:,0];
        KE_ratios = np.array(KE_of_ts)[:,-1] / np.array(KE_of_ts)[:,0];
        print("Difference of each particle: ", KE_differences)
        print("Average difference in initial KE to final KE: ", np.mean(KE_differences), " +/- ", np.std(KE_differences))
        print("Ratios of initial and final KE: ", KE_ratios);
        print("Average ratio of initial KE to final KE: ", np.mean(KE_ratios), " +/- ", np.std(KE_ratios))

        plt.legend();
        plt.show();

if __name__ == "__main__":
    main();
