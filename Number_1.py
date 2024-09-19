def series_resistance(resistors):
    """
    Calculate the equivalent resistance of resistors in series.
    """
    return sum(resistors)

def parallel_resistance(resistors):
    """
    Calculate the equivalent resistance of resistors in parallel.
    """
    reciprocal_sum = 0

    for r in resistors:
        if isinstance(r, (list, tuple)):
            # If r is a nested combination (list or tuple), compute its resistance
            r_value = equivalent_resistance(r)
        else:
            r_value = r
        reciprocal_sum += 1 / r_value

    if reciprocal_sum == 0:
        return float('inf')  # Handle open circuit case
    return 1 / reciprocal_sum

def equivalent_resistance(circuit):
    """
    Compute the resistance of a circuit that can have both series and parallel components.
    """
    result = 0
    for element in circuit:
        if isinstance(element, list):
            # Series combination
            result += series_resistance(element)
        elif isinstance(element, tuple):
            # Parallel combination
            result += parallel_resistance(element)
        else:
            # Single resistor
            result += element
    return result

def get_resistor_value():
    """
    Ask the user for a resistor value.
    """
    while True:
        try:
            r_value = float(input("Enter resistor value (in ohms): "))
            return r_value
        except ValueError:
            print("Invalid input. Please enter a numerical value.")

def get_series_or_parallel():
    """
    Ask the user if they want to create a series or parallel combination.
    """
    while True:
        choice = input("Is this a series (s) or parallel (p) combination? Enter 's' or 'p': ").lower()
        if choice in ['s', 'p']:
            return choice
        else:
            print("Invalid choice. Please enter 's' for series or 'p' for parallel.")

def create_circuit():
    """
    Create a circuit interactively by asking the user for series and parallel combinations.
    """
    circuit = []

    while True:
        add_resistor = input("Would you like to add a resistor or a combination? (yes/no): ").lower()
        if add_resistor == 'no':
            break

        choice = get_series_or_parallel()

        if choice == 's':
            num_resistors = int(input("How many resistors are in this series combination? "))
            series_resistors = [get_resistor_value() for _ in range(num_resistors)]
            circuit.append(series_resistors)
        elif choice == 'p':
            num_resistors = int(input("How many resistors are in this parallel combination? "))
            parallel_resistors = tuple(get_resistor_value() for _ in range(num_resistors))
            circuit.append(parallel_resistors)

    return circuit

# Main program
print("Welcome to the Circuit Simulator!")
print("You can enter resistors connected in series and parallel combinations.")

while True:
    circuit = create_circuit()
    if circuit:
        resistance = equivalent_resistance(circuit)
        print(f"The equivalent resistance of the circuit is: {resistance} Ω")
    else:
        print("No circuit created.")

    another_circuit = input("Would you like to create another circuit? (yes/no): ").lower()
    if another_circuit == 'no':
        break

print("Thank you for using the Circuit Simulator!")