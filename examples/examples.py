from netto import TaxConfig, calc_inverse_netto, calc_netto

# ============================================================================
# Basic Usage (using default configuration)
# ============================================================================

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


# ============================================================================
# Advanced Usage (using custom configuration)
# ============================================================================

# Create a custom configuration for a married person with children in 2025
config_2025_married = TaxConfig(
    year=2025,
    is_married=True,
    has_children=True,
    church_tax=0.0,  # No church tax
    extra_health_insurance=0.015,  # Slightly higher health insurance
)

# Calculate with custom configuration
net_income = calc_netto(60000, config=config_2025_married)
print(f"Net income for married person with children in 2025: {net_income}")

# Calculate inverse with custom configuration
gross_needed = calc_inverse_netto(45000, config=config_2025_married)
print(f"Gross salary needed to reach 45,000 net: {gross_needed}")


# Create a configuration for a single person without church tax in 2024
config_2024_single = TaxConfig(year=2024, is_married=False, has_children=False, church_tax=0.0)

# Calculate with different configuration
net_income_single = calc_netto(50000, config=config_2024_single, verbose=True)


# Multiple scenarios comparison
scenarios = [
    ("Single, 2024, no church tax", TaxConfig(year=2024, church_tax=0.0)),
    ("Married, 2024, with church tax", TaxConfig(year=2024, is_married=True, church_tax=0.09)),
    ("Single with children, 2025", TaxConfig(year=2025, has_children=True, church_tax=0.0)),
]

salary = 70000
print(f"\nComparison for {salary} EUR gross salary:")
print("-" * 60)
for description, config in scenarios:
    net = calc_netto(salary, config=config)
    print(f"{description:40} -> {net:10.2f} EUR")
