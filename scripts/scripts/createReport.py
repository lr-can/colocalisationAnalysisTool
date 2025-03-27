import os
from datetime import datetime
import argparse

def initialize(basename):
    """
    Initializes the final report by copying the template content to the output directory.
    Args:
        basename (str): The basename of the output
    """
    with open("../../ressources/template_res.html", "r") as file:
        template = file.read()
        # Create the output directory if it doesn't exist
        output_dir = f"../results/final_results/{basename}"
        os.makedirs(output_dir, exist_ok=True)

        current_date = datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.now().strftime("%H:%M:%S")
        # Write the template content to the final report file
        with open(os.path.join(output_dir, "final_report.html"), "w") as output_file:
            output_file.write(template.replace("{{DATE}}", current_date).replace("{{TIME}}", current_time))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a final report based on a template.")
    parser.add_argument("-i", "--initialize", action="store_true", help="Run the initialization script to create the final report.")
    parser.add_argument("-b", "--basename", type=str, help="Base name of the output files.")
    args = parser.parse_args()

    if args.initialize:
        initialize(args.basename)
        print(f"Final report initialized in ../results/final_results/{args.basename}/final_report.html")