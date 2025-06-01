from pathlib import Path
from pypdf import PdfWriter
from termcolor import colored

writer = PdfWriter()

def merge(files):
    print("\nWorking on it...")
    for i, pdf in enumerate(files):
        writer.append(pdf)
        print(colored(f"{i+1} Done!", "blue", attrs=["bold"]))

def export(export_path):
    export_path = Path(export_path)
    if not export_path.parent.exists():
        print("\nCreating Directory...")
        export_path.parent.mkdir(parents=True, exist_ok=True)
    else:
        print()
    print("Saving the Merged File...")
    writer.write(export_path)
    writer.close()
    return export_path

