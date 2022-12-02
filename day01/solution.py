import numpy as np

def read_calories_from_file(file_name: str) -> list:
    calories_list = []
    calories = 0
    with open(file_name, "r") as f:
        for line in f:
            val = line.rstrip()
            if val == "":
                calories_list.append(calories)
                calories = 0
            else:
                calories += int(val)

        calories_list.append(calories) # last entry

    return calories_list

# Part 1
calories_list = read_calories_from_file("input_calories.txt")
calories_max = np.max(calories_list)
elf_max = np.argmax(calories_list)+1
print(f"Max calories: {calories_max} (elf {elf_max})")

# Part 2
calories_list.sort(reverse=True)
calories_top_three = calories_list[:3]
print(f"Top three calories: {calories_top_three} (sum: {np.sum(calories_top_three)})")

