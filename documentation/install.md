# Project Documentation

## Overview

This project is based on analyzing the colocalization of prophages and defense systems in bacterial genomes to better understand the defense mechanisms that bacteria develop against bacteriophages. Bacteriophages can integrate into the bacterial genome in the lysogenic state. Some of these phages carry genes that encode restriction or exclusion proteins, which prevent other phages from infecting the bacterium, providing a defense mechanism by blocking superinfection. Additionally, some phages provide beneficial genes that improve antibiotic resistance or environmental adaptation, helping bacteria survive under hostile conditions.

ColocAtools is designed for analyzing the colocalization of prophages and defense systems in bacterial genomes to detect if defense systems are provided by the phages. The importance of this study lies in facilitating phage therapy, which uses phages (that do not develop defense systems) for treatment.
## Tools Used

For this, we will use three bioinformatics tools:

- **DefenseFinder**: This tool is based on identifying anti-phage defense systems in bacterial genomes.
- **geNomad**: This tool looks for mobile elements (provirus, plasmid, etc..) that can be transferred between organisms.
- **PHASTEST**: This tool is designed to identify and annotate prophages in bacterial genomes. PHASTEST offers an API, which creates a waiting list and there may be a delay in obtaining results, so the processing time can be longer, especially when the contigs are larger or more complex.
ColocAtools will then cross-check the results of these tools to provide a list of prophages and defense systems that overlap in the genome.
## Project Workflow

The project workflow consists of:

1. Installing the dependencies:
   - Conda
   - HMMER
   - DefenseFinder 
   - geNomad
   - PHASTETS
   - jq
   - pandas, plotly and ipywidgets.

2. Running geNomad and DefenseFinder and PHASTEST.

3. Analyzing colocalization.

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
