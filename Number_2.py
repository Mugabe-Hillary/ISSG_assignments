import numpy as np
import matplotlib.pyplot as plt

# Constants
R = 10000  # Resistance in ohms (10kΩ)
C = 0.00047  # Capacitance in farads (470µF)
V_source = 5  # Source voltage in volts (5V)
time_constant = R * C  # Time constant τ = RC

# Time setup
t_max = 5 * time_constant  # Simulate for 5 time constants
time_steps = 1000  # Number of steps in the simulation
time = np.linspace(0, t_max, time_steps)  # Time array

# Charging voltage function
def capacitor_charging(t, V_source, R, C):
    return V_source * (1 - np.exp(-t / (R * C)))

# Discharging voltage function
def capacitor_discharging(t, V_initial, R, C):
    return V_initial * np.exp(-t / (R * C))

# Simulate the charging phase
voltage_charging = capacitor_charging(time, V_source, R, C)

# Simulate the discharging phase (starting from the max charged voltage)
voltage_discharging = capacitor_discharging(time, V_source, R, C)

# Plot the results
plt.figure(figsize=(10, 6))

# Plot charging curve
plt.plot(time, voltage_charging, label="Charging", color="blue")

# Plot discharging curve
plt.plot(time, voltage_discharging, label="Discharging", color="red", linestyle="--")

# Adding titles and labels
plt.title("Capacitor Charging and Discharging in an RC Circuit")
plt.xlabel("Time (seconds)")
plt.ylabel("Voltage (V)")
plt.grid(True)

# Add a legend
plt.legend()

# Display the plot
plt.show()
