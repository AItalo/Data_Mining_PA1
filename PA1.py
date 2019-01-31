from tabulate import tabulate
import sys

def log(message):
    f = open("log.txt", "a")
    f.write(message + "\n")
    f.close()

'''
--------------------------------------------------
Setup Code
--------------------------------------------------
'''

f = open("log.txt", "w")
f.close()

args = sys.argv
if len(args) < 3:
    mpg = "auto-mpg.txt"
    prices = "auto-prices.txt"
else:
    mpg = args[1]
    prices = args[2]


data = "auto-data.txt"
mpg_nodups = mpg.strip(".txt") + "-nodups.txt"
prices_nodups_original = prices.strip(".txt") + "-nodups.txt"
prices_nodups = prices_nodups_original.strip(".txt") + "-clean.txt"
data_nodups = data.strip(".txt") + "-nodups.txt"
combined_table_1 = "combined-table-1.txt"
combined_table_1_nodups = combined_table_1.strip(".txt") + "-nodups.txt"
combined_table_2 = "combined-table-2.txt"
combined_table_2_nodups = combined_table_2.strip(".txt") + "-nodups.txt"
combined_table_3 = "combined-table-3.txt"
combined_table_3_nodups = combined_table_3.strip(".txt") + "-nodups.txt"
print()
print()



'''
--------------------------------------------------
Step 1
--------------------------------------------------
'''

# counts number of instances in a given dataset
# returns number of instances
def count_instances(file_path):
    log("Counting instances in " + file_path + "...")
    f = open(file_path, "r")
    count = 0
    while (f.readline() != ''):
        count += 1
    f.close()
    log("Found: " + str(count) + " instances")
    log("")
    return count

# detects duplicates in a given file and creates a new, duplicate-free file
# returns list of duplicates
def resolve_duplicates(file_path):
    f = open(file_path, "r")
    log("Scanning " + file_path + " for duplicates...")
    set = []
    duplicates = []

    line_i = f.readline()
    while (line_i != ''):
        if line_i in set:
            duplicates.append(line_i)
            log("duplicate found: [" + line_i.strip() + "]")
        else:
            set.append(line_i)
        line_i = f.readline()
    f.close()

    new_file_path = file_path.strip(".txt")
    new_file_path += "-nodups.txt"
    f = open(new_file_path, "w")
    for line in set:
        f.write(line)
    f.close()
    return duplicates



'''
--------------------------------------------------
Step 2
--------------------------------------------------
'''

# Combines datasets, writes result to auto-data.txt
# returns joined dataset
def join_datasets(mpg_file_path, prices_file_path, joined_file_path):
    log("joining datasets " + mpg_file_path + " and " + prices_file_path + "...")
    mpg_dataset = convert_dataset(mpg_file_path)
    prices_dataset = convert_dataset(prices_file_path)
    joined = []

    # join matches
    for price in prices_dataset:
        for mpg in mpg_dataset:
            if (price[0] == mpg[8]) and (price[1] == mpg[6]):
                instance = mpg
                instance.append(price[2])
                joined.append(instance)
                break
    
    # join non-matches from prices
    for price in prices_dataset:
        match = False
        for mpg in mpg_dataset:
            if (price[0] == mpg[8]) and (price[1] == mpg[6]):
                match = True
                break
        if match == False:
            instance = ["NA", "NA", "NA", "NA", "NA", "NA", price[1], "NA", price[0], price[2]]
            log("Found non-match in " + prices_file_path + ": " + str(instance))
            joined.append(instance)
    
    # join non-matches from mpg
    for mpg in mpg_dataset:
        match = False
        for price in prices_dataset:
            if (price[0] == mpg[8]) and (price[1] == mpg[6]):
                match = True
                break
        if match == False:
            instance = mpg
            instance.append("NA")
            log("Found non-match in " + mpg_file_path + ": " + str(instance))
            joined.append(instance)

    # write to auto-data.txt
    log("Writing dataset to " + joined_file_path + "...")
    f = open(joined_file_path, "w")
    for instance in joined:
        instance_str = []
        for elem in instance:
            instance_str.append(str(elem))
        write_str = ",".join(instance_str)
        write_str += "\n"
        f.write(write_str)
    log("")
    return joined


# Reads data file and creates a 2D array
# converts numbers to int
# returns array
def convert_dataset(file_path):
    log("Creating type-corrected dataset from " + file_path + "...")
    f = open(file_path, "r")
    dataset = []
    line = f.readline()
    while (line != ''):
        instance_r = line.strip().split(",")
        instance = []
        for elem in instance_r:
            try:
                instance.append(int(elem))
            except ValueError:
                try:
                    instance.append(float(elem))
                except ValueError:
                    instance.append(elem)
        dataset.append(instance)
        line = f.readline()
    f.close()
    return dataset


'''
--------------------------------------------------
Step 4
--------------------------------------------------
'''

# Calculates the minimum of all numerical values for a given dataset at a given index
# Ignores strings, such as NA
# returns minimum value
def calculate_minimum(dataset, index):
    minimum = dataset[0][index]
    for instance in dataset:
        if type(instance[index]) == str:
            continue
        elif instance[index] < minimum:
            minimum = instance[index]
    log("Found minimum value: " + str(minimum))
    return minimum


# Calculates the maximum of all numerical values for a given dataset at a given index
# Ignores strings, such as NA
# returns maximum value
def calculate_maximum(dataset, index):
    maximum = dataset[0][index]
    for instance in dataset:
        if type(instance[index]) == str:
            continue
        elif instance[index] > maximum:
            maximum = instance[index]
    log("Found maximum value: " + str(maximum))
    return maximum


# Calculates the midpoint of all numerical values for a given dataset at a given index
# Ignores strings, such as NA
# returns midpoint value
def calculate_midpoint(dataset, index):
    maximum = dataset[0][index]
    for instance in dataset:
        if type(instance[index]) == str:
            continue
        elif instance[index] > maximum:
            maximum = instance[index]
    
    minimum = dataset[0][index]
    for instance in dataset:
        if type(instance[index]) == str:
            continue
        elif instance[index] < minimum:
            minimum = instance[index]
    
    mid = (maximum + minimum) / 2
    log("Found midpoint value: " + str(mid))
    return mid

# Calculates the average of all numerical values for a given dataset at a given index
# Ignores strings, such as NA
# returns maximum value
def calculate_average(dataset, index):
    total = 0
    count = 0
    for instance in dataset:
        if type(instance[index]) == str:
            continue
        else:
            total += instance[index]
            count += 1
    average = float(total) / count
    log("Found average value: " + str(average))
    return average


# Calculates the median of all numerical values for a given dataset at a given index
# Ignores strings, such as NA
# returns median value
def calculate_median(dataset, index):
    values = []
    for instance in dataset:
        if type(instance[index]) == str:
            continue
        else:
            values.append(instance[index])
    values.sort()
    i = int(len(values) / 2)
    median = values[i]
    log("Found median value: " + str(median))
    return median



'''
--------------------------------------------------
Step 5
--------------------------------------------------
'''

# Approach 1: Remove Missing Values
# Removes all instances with missing values from auto-data.txt
# returns dataset with NA instances removed
def remove_missing_instances(file_path):
    log("Removing all instances with missing values from " + file_path + "...")
    dataset_i = convert_dataset(file_path)
    cleaned_data = []
    for instance in dataset_i:
        if "NA" in instance:
            continue
        else:
            cleaned_data.append(instance)
    log("Writing dataset to " + combined_table_1 + "...")
    f = open(combined_table_1, "w")
    for instance in cleaned_data:
        instance_str = []
        for elem in instance:
            instance_str.append(str(elem))
        write_str = ",".join(instance_str)
        write_str += "\n"
        f.write(write_str)
    f.close()
    log("")
    return cleaned_data


# Approach 2: Replace with average values
# Replaces all missing values with the average for that attribute
# returns dataset with all NA instances replaced
def replace_with_average(file_path):
    log("Replacing all missing values with averages for that attribute...")
    dataset_i = convert_dataset(file_path)
    log("mpg:")
    mpg_avg = calculate_average(dataset_i, 0)
    log("cylinders:")
    cylinders_avg = calculate_average(dataset_i, 1)
    log("displacement:")
    displacement_avg = calculate_average(dataset_i, 2)
    log("horsepower:")
    horsepower_avg = calculate_average(dataset_i, 3)
    log("weight:")
    weight_avg = calculate_average(dataset_i, 4)
    log("acceleration:")
    acceleration_avg = calculate_average(dataset_i, 5)
    log("model year:")
    year_avg = calculate_average(dataset_i, 6)
    log("origin:")
    origin_avg = calculate_average(dataset_i, 7)
    log("msrp:")
    msrp_avg = calculate_average(dataset_i, 9)

    averages = [mpg_avg, cylinders_avg, displacement_avg, horsepower_avg,
                weight_avg, acceleration_avg, year_avg, origin_avg, "MODEL", msrp_avg]

    cleaned_dataset = []

    for instance in dataset_i:
        cleaned_instance = []
        for x in range(len(instance)):
            if instance[x] == "NA":
                cleaned_instance.append(averages[x])
            else:
                cleaned_instance.append(instance[x])
        cleaned_dataset.append(cleaned_instance)

    log("Writing dataset to " + combined_table_2 + "...")
    f = open(combined_table_2, "w")
    for instance in cleaned_dataset:
        instance_str = []
        for elem in instance:
            instance_str.append(str(elem))
        write_str = ",".join(instance_str)
        write_str += "\n"
        f.write(write_str)
    f.close()
    log("")
    return cleaned_dataset


# Calculates the average for a given index of all cars with the same model year
# returns an average value
def calculate_average_year(dataset, index, year):
    total = 0
    count = 0
    for instance in dataset:
        if instance[index] == "NA":
            continue
        elif instance[6] == year:
            total += instance[index]
            count += 1
    average = total / count
    return average


# Approach 3: Replace with meaningful average
# Replaces all missing values with the average from instances with the same model year
# returns dataset with all NA values replaced
def replace_with_restricted_average(file_path):
    log("Replacing all missing values with averages for that attribute from instances with the same model year...")
    dataset_i = convert_dataset(file_path)
    log("If model year is NA, will be replaced with average for year:")
    year_avg = calculate_average(dataset_i, 6)

    cleaned_dataset = []

    for instance in dataset_i:
        cleaned_instance = []
        for x in range(len(instance)):
            if instance[x] == "NA":
                if x == 6:
                    cleaned_instance.append(year_avg)
                else:
                    cleaned_instance.append(calculate_average_year(dataset_i, x, instance[6]))
            else:
                cleaned_instance.append(instance[x])
        cleaned_dataset.append(cleaned_instance)

    log("Writing dataset to " + combined_table_3 + "...")
    f = open(combined_table_3, "w")
    for instance in cleaned_dataset:
        instance_str = []
        for elem in instance:
            instance_str.append(str(elem))
        write_str = ",".join(instance_str)
        write_str += "\n"
        f.write(write_str)
    f.close()
    log("")
    return cleaned_dataset


'''
--------------------------------------------------
Final Script
--------------------------------------------------
'''

count_mpg = count_instances(mpg)
count_prices = count_instances(prices)

log("Resolving duplicates by creating a set of unique lines from original file and writing modified dataset to new file")
dups_mpg = resolve_duplicates(mpg)
dups_prices = resolve_duplicates(prices)
log("")

count_mpg_nodups = count_instances(mpg_nodups)
count_prices_nodups = count_instances(prices_nodups)

join_datasets(mpg_nodups, prices_nodups, data)

count_joined = count_instances(data)
dups_joined = resolve_duplicates(data)
count_joined_nodups = count_instances(data_nodups)


log("Manual clean up of " + prices_nodups_original + ":")
log('For models with initial non-match ["audi 100 ls", "bmw 2002", "chevy c20", "dodge d200", "ford f250", "peugeot 504", "saab 99e"] : ')
log("Instance of model exists in " + prices_nodups_original + "with model year 71, while separate instance of model exists in " + mpg_nodups + " with model year 70 and no match." )
log("Cases resolved by editing " + prices_nodups_original + " and changing model year to match instance in " + mpg_nodups)
log("New dataset saved in " + prices_nodups)
log('For model with initial non-match ["toyoto corona mark ii (sw)"] :')
log('Misspelling of "toyoto", corrected to "toyota"')
log("")

dataset = convert_dataset(data_nodups)
log("")


def create_tabulate_row(attribute, dataset, index):
    log("Calculating statistics for: " + attribute)
    row = [attribute, calculate_minimum(dataset, index), calculate_maximum(dataset, index), calculate_midpoint(dataset, index), calculate_average(dataset, index), calculate_median(dataset, index)]
    log("")
    return row

mpg_stats = create_tabulate_row("mpg", dataset, 0)
cylinders_stats = create_tabulate_row("cylinders", dataset, 1)
displacement_stats = create_tabulate_row("displacement", dataset, 2)
horsepower_stats = create_tabulate_row("horsepower", dataset, 3)
weight_stats = create_tabulate_row("weight", dataset, 4)
acceleration_stats = create_tabulate_row("acceleration", dataset, 5)
year_stats = create_tabulate_row("model year", dataset, 6)
origin_stats = create_tabulate_row("origin", dataset, 7)
msrp_stats = create_tabulate_row("msrp ", dataset, 9)

table = [mpg_stats, cylinders_stats, displacement_stats, horsepower_stats, weight_stats, acceleration_stats, year_stats, origin_stats, msrp_stats]
header = ["attribute", "min", "max", "mid", "avg", "med"]

cleaned_dataset_1 = remove_missing_instances(data_nodups)
count_combined_1 = count_instances(combined_table_1)
dups_combined_1 = resolve_duplicates(combined_table_1)
count_combined_1_nodups = count_instances(combined_table_1_nodups)

log("")
cleaned_table_1 = [create_tabulate_row("mpg", cleaned_dataset_1, 0), 
                    create_tabulate_row("cylinders", cleaned_dataset_1, 1), 
                    create_tabulate_row("displacement", cleaned_dataset_1, 2), 
                    create_tabulate_row("horsepower", cleaned_dataset_1, 3), 
                    create_tabulate_row("weight", cleaned_dataset_1, 4), 
                    create_tabulate_row("acceleration", cleaned_dataset_1, 5), 
                    create_tabulate_row("model year", cleaned_dataset_1, 6), 
                    create_tabulate_row("origin", cleaned_dataset_1, 7),
                    create_tabulate_row("msrp", cleaned_dataset_1, 9)]


cleaned_dataset_2 = replace_with_average(data_nodups)
count_combined_2 = count_instances(combined_table_2)
dups_combined_2 = resolve_duplicates(combined_table_2)
count_combined_2_nodups = count_instances(combined_table_2_nodups)

log("")

cleaned_table_2 = [create_tabulate_row("mpg", cleaned_dataset_2, 0), 
                    create_tabulate_row("cylinders", cleaned_dataset_2, 1), 
                    create_tabulate_row("displacement", cleaned_dataset_2, 2), 
                    create_tabulate_row("horsepower", cleaned_dataset_2, 3), 
                    create_tabulate_row("weight", cleaned_dataset_2, 4), 
                    create_tabulate_row("acceleration", cleaned_dataset_2, 5), 
                    create_tabulate_row("model year", cleaned_dataset_2, 6), 
                    create_tabulate_row("origin", cleaned_dataset_2, 7),
                    create_tabulate_row("msrp", cleaned_dataset_2, 9)]


cleaned_dataset_3 = replace_with_restricted_average(data_nodups)
count_combined_3 = count_instances(combined_table_3)
dups_combined_3 = resolve_duplicates(combined_table_3)
count_combined_3_nodups = count_instances(combined_table_3_nodups)

log("")

cleaned_table_3 = [create_tabulate_row("mpg", cleaned_dataset_3, 0), 
                    create_tabulate_row("cylinders", cleaned_dataset_3, 1), 
                    create_tabulate_row("displacement", cleaned_dataset_3, 2), 
                    create_tabulate_row("horsepower", cleaned_dataset_3, 3), 
                    create_tabulate_row("weight", cleaned_dataset_3, 4), 
                    create_tabulate_row("acceleration", cleaned_dataset_3, 5), 
                    create_tabulate_row("model year", cleaned_dataset_3, 6), 
                    create_tabulate_row("origin", cleaned_dataset_3, 7),
                    create_tabulate_row("msrp", cleaned_dataset_3, 9)]


print("--------------------------------------------------")
print("auto-mpg.txt")
print("--------------------------------------------------")
print("No. of instances: " + str(count_mpg))
print("Duplicates: [", end = '')
for line in dups_mpg:
    print("[" + line.strip() + "]", end = '')
print("]")
print("No. of unique instances: " + str(count_mpg_nodups))
print("--------------------------------------------------")
print("auto-prices.txt")
print("--------------------------------------------------")
print("No. of instances: " + str(count_prices))
print("Duplicates: [", end = '')
for line in dups_prices:
    print("[" + line.strip() + "]", end = '')
print("]")
print("No. of unique instances: " + str(count_prices_nodups))
print("--------------------------------------------------")
print("Combined table (saved as auto-data.txt)")
print("--------------------------------------------------")
print("No. of instances: " + str(count_joined))
print("Duplicates: [", end = '')
for line in dups_joined:
    print("[" + line.strip() + "]", end = '')
print("]")
print("No. of unique instances: " + str(count_joined_nodups))
print("Summary Stats:")
print(tabulate(table, headers=header))
print("--------------------------------------------------")
print("Combined table (rows w/ missing values removed)")
print("--------------------------------------------------")
print("No. of instances: " + str(count_combined_1))
print("Duplicates: [", end = '')
for line in dups_combined_1:
    print("[" + line.strip() + "]", end = '')
print("]")
print("No. of unique instances: " + str(count_combined_1_nodups))
print("Summary Stats:")
print(tabulate(cleaned_table_1, headers=header))
print("--------------------------------------------------")
print("Combined table (missing values replaced w/ average)")
print("--------------------------------------------------")
print("No. of instances: " + str(count_combined_2))
print("Duplicates: [", end = '')
for line in dups_combined_2:
    print("[" + line.strip() + "]", end = '')
print("]")
print("No. of unique instances: " + str(count_combined_2_nodups))
print("Summary Stats:")
print(tabulate(cleaned_table_2, headers=header))
print("--------------------------------------------------")
print("Combined table (missing values replaced w/ average based on model year)")
print("--------------------------------------------------")
print("No. of instances: " + str(count_combined_3))
print("Duplicates: [", end = '')
for line in dups_combined_3:
    print("[" + line.strip() + "]", end = '')
print("]")
print("No. of unique instances: " + str(count_combined_3_nodups))
print("Summary Stats:")
print(tabulate(cleaned_table_3, headers=header))
