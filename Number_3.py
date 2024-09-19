import numpy as np

# Step 1: Input data for line impedances, power, and initial voltages
def get_system_data():
    # Get number of buses from user
    num_buses = int(input("Enter the number of buses: "))
    
    # Assuming the number of lines is num_buses*(num_buses-1)/2 for a fully connected system
    num_lines = int(input("Enter the number of lines in the system: "))

    # Line impedance data (assuming user provides impedance in complex form)
    Z_lines = []
    for i in range(num_lines):
        z = complex(input(f"Enter the impedance (r+jx) for line {i+1}: "))
        Z_lines.append(z)

    # Active and reactive power for generation (P_G, Q_G) and loads (P_L, Q_L)
    P_G = np.zeros(num_buses)
    Q_G = np.zeros(num_buses)
    P_L = np.zeros(num_buses)
    Q_L = np.zeros(num_buses)

    for i in range(1, num_buses):
        P_L[i] = float(input(f"Enter the active power load at bus {i} (P_L[{i}]): "))
        Q_L[i] = float(input(f"Enter the reactive power load at bus {i} (Q_L[{i}]): "))

    # Assumed initial bus voltages
    V = np.zeros(num_buses, dtype=complex)
    for i in range(num_buses):
        V[i] = complex(input(f"Enter the initial voltage at bus {i} (in form a+bj): "))

    return num_buses, Z_lines, P_L, Q_L, V

# You will need to adapt the calculation of the Y-bus matrix for the actual number of lines.

# Step 2: Calculate Y-Bus Matrix with the specified relationships
def calculate_ybus(num_buses, Z_lines):
    Y_bus = np.zeros((num_buses, num_buses), dtype=complex)
    
    # Calculate admittances (1 / impedance)
    Y12 = 1 / Z_lines[0]  # Line between Bus 1 and Bus 2
    Y23 = 1 / Z_lines[1]  # Line between Bus 2 and Bus 3
    Y13 = 1 / Z_lines[2]  # Line between Bus 1 and Bus 3
    
    # Off-diagonal elements
    Y_bus[0, 1] = Y12  # y12
    Y_bus[1, 0] = Y12  # y21
    
    Y_bus[1, 2] = Y23  # y23
    Y_bus[2, 1] = Y23  # y32
    
    Y_bus[0, 2] = Y13  # y13
    Y_bus[2, 0] = Y13  # y31
    
    # Diagonal elements
    Y_bus[0, 0] = Y12 + Y13  # y11 = y12 + y13
    Y_bus[1, 1] = Y12 + Y23  # y22 = y21 + y23
    Y_bus[2, 2] = Y13 + Y23  # y33 = y31 + y32

    return Y_bus


# Step 3: Gauss-Seidel Iteration
def gauss_seidel(Y_bus, P_L, Q_L, V, num_buses, max_iterations=2):
    for iteration in range(max_iterations):
        for i in range(1, num_buses):
            # Calculate power mismatch and update voltages
            P_i = P_L[i]
            Q_i = Q_L[i]
            sum_YV = sum(Y_bus[i, j] * V[j] for j in range(num_buses) if i != j)
            
            V[i] = (P_i - Q_i * 1j) / np.conj(V[i]) - sum_YV / Y_bus[i, i]
            V[i] = V[i] / np.abs(V[i])  # Normalize voltage

        print(f"Iteration {iteration+1}: Bus Voltages: {V}")
    
    return V

# Step 4: Calculate Slack Bus Power
def calculate_slack_bus_power(V, Y_bus):
    # Slack bus power is calculated using the voltages and admittance matrix
    slack_voltage = V[0]
    P_slack = np.real(np.conj(slack_voltage) * sum(Y_bus[0, j] * V[j] for j in range(len(V))))
    Q_slack = np.imag(np.conj(slack_voltage) * sum(Y_bus[0, j] * V[j] for j in range(len(V))))
    
    return P_slack, Q_slack

# Step 5: Calculate Line Flows and Losses
def calculate_line_flows_losses(V, Z_lines):
    # Assuming connections are: Line 1 -> Bus 0-1, Line 2 -> Bus 1-2, Line 3 -> Bus 0-2
    bus_pairs = [(0, 1), (1, 2), (0, 2)]
    
    line_flows = []
    line_losses = []

    for idx, (bus_i, bus_j) in enumerate(bus_pairs):
        I_line = (V[bus_i] - V[bus_j]) / Z_lines[idx]  # Current in the line
        S_flow = V[bus_i] * np.conj(I_line)  # Apparent power flow in the line
        S_loss = S_flow - V[bus_j] * np.conj(I_line)  # Loss in the line

        line_flows.append(S_flow)
        line_losses.append(S_loss)

    return line_flows, line_losses


# Main function
def main():
    # Step 1: Get user input
    num_buses, Z_lines, P_L, Q_L, V = get_system_data()
    
    # Step 2: Compute Y-bus matrix
    Y_bus = calculate_ybus(num_buses, Z_lines)
    print("Y-bus matrix: \n", Y_bus)

    # Step 3: Perform Gauss-Seidel Iteration
    V_final = gauss_seidel(Y_bus, P_L, Q_L, V, num_buses)

    # Step 4: Calculate slack bus power
    P_slack, Q_slack = calculate_slack_bus_power(V_final, Y_bus)
    print(f"Slack bus real power: {P_slack}, reactive power: {Q_slack}")

    # Step 5: Calculate line flows and losses
    line_flows, line_losses = calculate_line_flows_losses(V_final, Z_lines)
    print(f"Line Flows: {line_flows}")
    print(f"Line Losses: {line_losses}")

if __name__ == "__main__":
    main()
