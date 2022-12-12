from netto import calc_inverse_netto, calc_netto

# Calculate net income for a salary of 50,000 with no additional deductibles
calc_netto(50000)

# Calculate net income for a salary of 50,000 with additional deductibles of 10,000
calc_netto(50000, deductibles=10000)

# Calculate net income for a salary of 50,000 and print additional information
calc_netto(50000, deductibles=10000, verbose=True)

# Calculate gross salary needed to reach a net income of 50,000 with no additional deductibles
calc_inverse_netto(50000)

# Calculate gross salary needed to reach a net income of 50,000 with additional deductibles of 5,000
calc_inverse_netto(50000, deductibles=5000)