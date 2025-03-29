import os
from datetime import datetime
import argparse
import re

def initialize(basename):
    """
    Initializes the final report by copying the template content to the output directory.
    Args:
        basename (str): The basename of the output
    """
    with open("../ressources/template_res.html", "r") as file:
        template = file.read()
        # Create the output directory if it doesn't exist
        output_dir = f"./results/final_results/{basename}"
        os.makedirs(output_dir, exist_ok=True)

        current_date = datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.now().strftime("%H:%M:%S")
        # Write the template content to the final report file
        with open(os.path.join(output_dir, "final_report.html"), "w") as output_file:
            output_file.write(template.replace("{{DATE}}", current_date).replace("{{TIME}}", current_time))

def addPlot(basename, plot_html, tolerance, file_name, file_path, origin_id):
    """
    Adds a plot to the final report.
    Args:
        basename (str): The basename of the output
        plot_html (str): The HTML content of the plot
        tolerance (float): The tolerance used for the plot
    """
    output_dir = f"./results/final_results/{basename}"
    with open(os.path.join(output_dir, "final_report.html"), "r+") as output_file:
        content = output_file.read()
        h1_ele = ""
        if f"<h1 class=\"newFile\" id=\"{os.path.basename(file_path)}\">{os.path.basename(file_path)}</h1>" not in content:
            h1_ele = f"""
            <h1 class="newFile" id=\"{os.path.basename(file_path)}\">{os.path.basename(file_path)}</h1>
            """
        with open(file_path, "r") as file:
            lines = file.readlines()
            for line in lines[1:]:  # Skip the header
                columns = line.strip().split("\t")
                if origin_id == columns[0]:  # Check if origin_id matches the first column
                    tax_id = columns[14]
                    tax = columns[15]
                    break
            html_element = f"""
    {h1_ele}
    <div class="main" id="{file_name}">
        <h2>{file_name}</h2>
        <p>Tolerance: {tolerance} bp</p>
        <p>Provirus taxonomy: {tax} (<a href="https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id={tax_id}">{tax_id}</a>)</p>
        {plot_html}
    </div>
            """
            updated_content = content.replace("{{results}}", html_element + "{{results}}")
            output_file.seek(0)
            output_file.write(updated_content)
            output_file.truncate()

def createMenu(output_dir):
    """
    Parses the HTML file and creates a menu for the report from the h1.newFile tags.
    Args:
        output_dir (str): The output directory
    """
    with open(os.path.join(output_dir, "final_report.html"), "r+") as output_file:
        content = output_file.read()
        lines = content.splitlines()
        menu = []
        for line in lines:
            if "<h1 class=\"newFile\" id=\"" in line:
                match = re.search(r'id="([^"]+)"', line)
                if match:
                    menu.append(match.group(1))
        menu_html = "".join([f"<div><a href='#{item}'>{item}</a></div>" for item in menu])
        updated_content = content.replace("{{menu}}", menu_html)
        output_file.seek(0)
        output_file.write(updated_content)
        output_file.truncate()
        
def endReport(basename):
    """
    Adds the end of the final report.
    Args:
        basename (str): The basename of the output
    """
    output_dir = f"./results/final_results/{basename}"
    createMenu(output_dir)
    with open(os.path.join(output_dir, "final_report.html"), "r+") as output_file:
        content = output_file.read()
        updated_content = content.replace("{{results}}", "")
        output_file.seek(0)
        output_file.write(updated_content)
        output_file.truncate()
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a final report based on a template.")
    parser.add_argument("-i", "--initialize", action="store_true", help="Run the initialization script to create the final report.")
    parser.add_argument("-b", "--basename", type=str, help="Base name of the output files.")
    args = parser.parse_args()

    if args.initialize:
        initialize(args.basename)
        print(f"Final report initialized in results/final_results/{args.basename}/final_report.html")