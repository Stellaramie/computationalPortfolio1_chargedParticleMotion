# Computational Portfolio 1 - Charged particle motion
Using Python and SciPy to track the motion and kinetic energy of a charged particle in the presence of an electric and magnetic field.

## Usage
This code can produce plots for a set of hardcoded particle's trajectories and kinetic energies for an arbitrary magnetic field, $B_z$, and static electric field, $E$.

Use the `python3 ChargedParticleMotion.py --help` to get a list of optional parameters available to use.

Example use case - Plotting the particle trajectories and the kinetic energies over time with a slight electric field:
```
python3 ChargedParticleMotion.py -btk -E 0 0.01 
```

![The trajectories of four charged particles tracked through the magnetic field and homogenous electric field with strength $\hat{E}_y = 0.01$. The simulation takes place from $\hat{t} = 0$ until $\hat{t} = 500$. Homogenous electric field with strength $\hat{E}_y = 0.01$](traj_E=001.png)
The trajectories of four charged particles tracked through the magnetic field and homogenous electric field with strength $\hat{E}_y = 0.01$. The simulation takes place from $\hat{t} = 0$ until $\hat{t} = 500$. Homogenous electric field with strength $\hat{E}_y = 0.01$. Plot produced with command 'python3 ChargedParticleMotion.py -bt -E 0 0.01'.
