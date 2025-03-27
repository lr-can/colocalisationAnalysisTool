# Project Documentation

## Overview

This project is based on the analysis of prophage colocalization and defense systems in bacterial genomes, in order to better understand the defense mechanisms that bacteria develop against bacteriophages. Some of these phages carry genes encoding restriction or exclusion proteins, which prevent other phages from infecting the bacteria, thus providing a defense mechanism by blocking superinfection. In addition, some phages contain beneficial genes that enhance antibiotic resistance or environmental adaptation, helping bacteria to survive in hostile conditions.
Our aim is to develop a “ColocAtools” tool to analyze the colocalization of prophages and defense systems in bacterial genomes, in order to detect whether defense systems are provided by phages. The importance of this study lies in facilitating phage therapy, which uses phages (which do not develop defense systems) for treatments.
## Tools Used

For this, we will use three bioinformatics tools:

- **DefenseFinder**: This tool is based on identifying anti-phage defense systems in bacterial genomes.
- **geNomad**: This tool looks for mobile elements (provirus, plasmid, etc..) that can be transferred between organisms.
- **PHASTEST**: This tool is designed to identify and annotate prophages in bacterial genomes. PHASTEST offers an API, which creates a waiting list and there may be a delay in obtaining results, so the processing time can be longer, especially when the contigs are larger or more complex.
ColocAtools will then cross-check the results of these tools to provide a list of prophages and defense systems that overlap in the genome.
## Project Workflow

The project workflow consists of:

### 1. Installing the dependencies:
This tool relies on several bioinformatics dependencies that require specific versions, which may not be compatible with each other. To ensure proper installation and avoid conflicts between these versions, each tool will be installed in a separate Conda environment.
#### Prerequisites:
Before starting the installation process, ensure the following prerequisites are met:
Python 3 must be installed on your machine.
#### Installation Process:
1. Run the install.py file: 
  ````python3 install.py ```
   - The execution of the install.py file will activate a virtual environment, check if Conda is installed and accessible.

   - If Conda is not installed, restart the terminal and run install.py again after installing Conda.

   - The script will verify all required dependencies and create isolated Conda environments to install the following necessary tools and libraries:
      - Conda
      - HMMER
      - DefenseFinder 
      - geNomad
      - PHASTETS
      - jq
      - pandas, plotly and ipywidgets.
   - After running this script, the terminal must be restarted to ensure that everything has been installed correctly
2. Input data: 
To run ColocAtools, it is necessary to provide a FASTA file of nucleotide sequences, as Genomad requires nucleotide sequences, while DefenseFinder can work with both nucleotide and proteomic sequences.
3. Running geNomad and DefenseFinder and PHASTEST.
   1. Prophage Detection with Genomad
  After installing the necessary dependencies, the tool will run Genomad to search for prophages across the entire reference genome provided.
  ##### Output
  - The results will be stored in the following directory:
  results/results_genomad/<genome_name_without_extension>

  - The tool will focus on the file containing the constitutive genes of the different prophages and their genomic coordinates. This file is named:
    genome_name_virus_genes.tsv

  - This file can be found in the genome_name_summary directory.
  ##### Documentation
  For more information, refer to the official Genomad documentation:
  https://portal.nersc.gov/genomad/pipeline.html


  2. Identification of Defense Systems with Defense Finder:
   In this step, Defense Finder is launched to detect all known anti-phage systems based on its pipeline.
  ##### Output
  - The results from this step will be stored in the following directory:
  results/result_Finder/<genome_name_without_extension>

  - The tool will then intersect the following files for further analysis:

    genome_name.fa_defense_finder_genes.tsv

    genome_name.fa.prt_defensefinder.prt

  ##### Documentation
  For more information, refer to the official Defense Finder documentation:
  https://github.com/mdmparis/defense-finder



1. Analyzing colocalization.

## Scripts

We have two scripts that interact to carry this out:


## Script: install.py

This script activates the virtual environment in Python, checks if Conda is installed, and installs it locally if necessary. Additionally, it runs `checkOrInstall.sh`, which installs HMMER if it is not present on the system and also installs our tools: DefenseFinder, geNomad, and a Phastest API script. 

After running this script, the terminal needs to be relaunched to ensure that everything has been installed correctly.


## Script: run.py

This script allows running the colocalization analysis of defense systems and prophages in bacterial genomes.

### Parameters

- `-f / --file <file>`: Specifies a `.fa` or `.fasta` file to analyze.
- `-d / --directory <directory>`: Specifies a directory with multiple files to analyze.
- `-t / --threads <number>`: Number of threads to use in geNomad (optional). By default, the threads will be set to 4.
- `-p / --phastest`: Include if you also want to run phastest. 
### Results

The results are saved in:
- `results/result_Finder/` with the name of the file corresponding to the processed input file.
- `results/results_genomad/` with the name corresponding to the processed file.
- `results/results_phastest/` with the name corresponding to the processed file.


## Usage

To use the project, first ensure that all dependencies are installed correctly by running the `install.py` script. Then, you can execute the analysis using the `run.py` script, specifying the input files or directories and the desired number of threads.

## Example Usage

To illustrate the workflow, we provide a sample dataset and an example command to run the analysis.
### 1️⃣ Download an Example FASTA File
You can download a bacterial genome sequence directly from NCBI using:

```bash
wget -O NZ_PNSW01000002.1.fa "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=NZ_PNSW01000002.1&rettype=fasta&retmode=text"
```
### 2️⃣ Run the Analysis:
After installing dependencies using install.py, execute the analysis with:

python run.py -f NZ_PNSW01000002.1.fa -t 4 -p


## References

- **DefenseFinder**: Developed by MDMP Team (Institut Pasteur).  
  Repository: [https://github.com/mdmparis/DefenseFinder](https://github.com/mdmparis/DefenseFinder)  
  Publication: 
  [- Tesson, F., Hervé, A., Mordret, E., Touchon, M., d’Humières, C., Cury, J., & Bernheim, A. (2022). *Systematic and quantitative view of the antiviral arsenal of prokaryotes*. Nature Communications.]  
  [- Néron, B., Denise, R., Coluzzi, C., Touchon, M., Rocha, E. P. C., & Abby, S. S. (2023). *MacSyFinder v2: Improved modelling and search engine to identify molecular systems in genomes*. Peer Community Journal, 3, e28.]
  [  - Couvin, D., et al. (2018). *CRISPRCasFinder, an update of CRISRFinder, includes a portable version, enhanced performance and integrates search for Cas proteins*. Nucleic Acids Research.] 

- **geNomad**: Developed by PhiWeber Lab.  
  Repository: [https://github.com/phiweger/geNomad](https://github.com/phiweger/geNomad)  
  Publication: [  - Camargo, A. P., Roux, S., Schulz, F., Babinski, M., Xu, Y., Hu, B., Chain, P. S. G., Nayfach, S., & Kyrpides, N. C. (2023). *Identification of mobile genetic elements with geNomad*. Nature Biotechnology. DOI: [10.1038/s41587-023-01953-y](https://doi.org/10.1038/s41587-023-01953-y)]  

- **PHASTEST**: Developed by PhageParser Team.  
  Repository: [https://github.com/phageParser/PHASTEST](https://github.com/phageParser/PHASTEST)  
  Publication: [ - Wishart, D. S., Han, S., Saha, S., Oler, E., Peters, H., Grant, J., Stothard, P., & Gautam, V. (2023). *PHASTEST: Faster than PHASTER, Better than PHAST*. Nucleic Acids Research (Web Server Issue). DOI: [10.1093/nar/gkad382](https://doi.org/10.1093/nar/gkad382)]  
