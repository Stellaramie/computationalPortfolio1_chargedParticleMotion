import numpy as np
import matplotlib.pyplot as plt

# Function to calculate the magnetic field, vec_B,
# based on the position, vec_x.
def B_func(vec_x, B_0, x_0, x_c):
    x = vec_x[0];
    Bz = B_0 * x_0 / (x - x_c); # "y" is unused in this magnetic field.
    return Bz;

# Function to plot array_of_Bz at positions of x
def plot_B_func(array_of_xs, array_of_ys, array_of_Bzs):
    plt.pcolormesh(array_of_xs, array_of_ys, array_of_Bzs.T, shading = 'auto');
    plt.xlabel(r'$\hat{x}$ (normalised to thermal hydrogen gyro-radius, $ρ_H$)');
    plt.ylabel(r'$\hat{y}$ (normalised to thermal hydrogen gyro-radius, $ρ_H$)');
    plt.title(r"Example magnetic field in the z direction, $B_z$, at various points of $\hat{x}$ and $\hat{y}$");
    plt.colorbar(label=r'$B_z$ (normalised to radial magnetic field, $B_r$)');
    plt.show();

def df_dt(current_t, current_vec_x, B_0, x_0, x_c, q, m):
    v_x = current_vec_x[2];
    v_y = current_vec_x[3];
    B_z = B_func(current_vec_x, B_0, x_0, x_c);
    E_x = 0.;
    E_y = 0.;

    dx_dt = v_x;
    dy_dt = v_y;

    dv_x_dt = q * (E_x + v_y * B_z) / m;
    dv_y_dt = q * (E_y + v_x * B_z) / m;

    return [dx_dt, dy_dt, dv_x_dt, dv_x_dt];

def solve_df_dt()

def main():
    # Plot the magnetic field over an area within the x-y plain.
    # ----------------------------------------------------------

    # Create x-y values for which to calculate Bz.
    number_of_xs = 1001; # Called "nx" in the script.
    number_of_ys = 501; # Called "ny" in the script.
    max_value_of_x = 100.0; # Called "L_x" in the script.
    max_value_of_y = 50.0; # Called "L_y" in the script.
    array_of_xs = np.linspace(0, max_value_of_x, number_of_xs); # Called "xx" in the script.
    array_of_ys = np.linspace(0, max_value_of_y, number_of_ys); # Called "yy" in the script.

    # Initialise Bz array.
    array_of_Bzs = np.zeros([number_of_xs, number_of_ys]); # Called "Bmag" in the script.

    # Calculate constants.
    x_0 = max_value_of_x / 2;
    x_c = -max_value_of_x;
    B_0 = 1.0;

    # Calculate Bz at point (x, y).
    for ix, x in enumerate(array_of_xs):
        for iy, y in enumerate(array_of_ys):
            vec_x = np.array([x, y]);
            array_of_Bzs[ix, iy] = B_func(vec_x, B_0, x_0, x_c);


    plot_B_func(array_of_xs, array_of_ys, array_of_Bzs);

if __name__ == "__main__":
    main();