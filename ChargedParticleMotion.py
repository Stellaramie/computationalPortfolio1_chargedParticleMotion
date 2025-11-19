import numpy as np
import matplotlib.pyplot as plt

# Function to calculate the magnetic field, vec_B_hat,
# based on the position, vec_x_hat.
def B_func(vec_x_hat, B_0, x_0, x_c):
    x_hat = vec_x_hat[0];
    Bz_hat = B_0 * x_0 / (x_hat - x_c);
    return Bz_hat;

# Function to plot array_of_Bz_hat at positions of x
def plot_B_func(array_of_x_hats, array_of_y_hats, array_of_Bz_hats):
    plt.pcolormesh(array_of_x_hats, array_of_y_hats, array_of_Bz_hats.T, shading = 'auto');
    plt.xlabel(r'$\hat{x}$ (normalised to thermal hydrogen gyro-radius, $ρ_H$)');
    plt.ylabel(r'$\hat{y}$ (normalised to thermal hydrogen gyro-radius, $ρ_H$)');
    plt.title(r"Example magnetic field in the z direction, $B_z$, at various points of $\hat{x}$ and $\hat{y}$");
    plt.colorbar(label=r'$B_z$ (normalised to radial magnetic field, $B_r$)');
    plt.show();

def main():
    # Plot the magnetic field over an area within the x-y plain.
    # ----------------------------------------------------------

    # Create x-y values for which to calculate Bz_hat.
    number_of_x_hats = 1001; # Called "nx" in the script.
    number_of_y_hats = 501; # Called "ny" in the script.
    max_value_of_x_hat = 100.0; # Called "L_x" in the script.
    max_value_of_y_hat = 50.0; # Called "L_y" in the script.
    array_of_x_hats = np.linspace(0, max_value_of_x_hat, number_of_x_hats); # Called "xx" in the script.
    array_of_y_hats = np.linspace(0, max_value_of_y_hat, number_of_y_hats); # Called "yy" in the script.

    # Initialise Bz_hat array.
    array_of_Bz_hats = np.zeros([number_of_x_hats, number_of_y_hats]); # Called "Bmag" in the script.

    # Calculate constants.
    x_0 = max_value_of_x_hat / 2;
    x_c = -max_value_of_x_hat;
    B_0 = 1.0;

    # Calculate Bz_hat at point (x, y).
    for ix, x in enumerate(array_of_x_hats):
        for iy, y in enumerate(array_of_y_hats):
            vec_x_hat = np.array([x, y]);
            array_of_Bz_hats[ix, iy] = B_func(vec_x_hat, B_0, x_0, x_c);


    plot_B_func(array_of_x_hats, array_of_y_hats, array_of_Bz_hats);

if __name__ == "__main__":
    main();