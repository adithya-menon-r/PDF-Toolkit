from pathlib import Path
from tabulate import tabulate 
from termcolor import colored

def display_file_order(files):
    file_order = [
        {"No.": i+1, "File Name": Path(file_path).parts[-1]} for i, file_path in enumerate(files)
    ]
    print(tabulate(file_order, headers="keys", tablefmt="rounded_grid"))

def reorder_files(files):
    while True:
        try:
            new_order = input("\nEnter the file numbers in the required order (seperated by ',' or ' ').\n>> ").strip()
            new_order = new_order.replace("\"", "")
            order_index = new_order.split(",") if "," in new_order else new_order.split()
            if len(order_index) != len(set(order_index)) != len(files):
                raise IndexError
            reordered_files = [files[int(index) - 1] for index in order_index]
            break
        except (ValueError, IndexError):
            print(colored(f"ERROR: Invalid Order. Reordering couldn't be processed. Try typing the order like \"5,2,1,3,4\".", "red", attrs=["bold"]))
    return reordered_files
