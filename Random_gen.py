import random

# Get user input for the total number of entries available
num_entries = int(input("Enter the total number of entries: "))

# Check if the number of entries is greater than or equal to 4
if num_entries < 4:
    print("The number of entries must be at least 4.")
else:
    # Randomly select 4 unique numbers from the range 1 to num_entries
    random_selection = random.sample(range(1, num_entries + 1), 4)

    # Print the randomly selected numbers
    print("Randomly selected numbers:", random_selection)
