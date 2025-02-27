#!/bin/bash
export PATH=.venv/:$PATH

condition=0
# Install HMMER if not found
if ! command -v hmmsearch &> /dev/null
then
    echo "hmmsearch could not be found, installing..."
    mkdir -p $HOME/tmp
    wget http://eddylab.org/software/hmmer/hmmer.tar.gz -O $HOME/tmp/hmmer.tar.gz
    tar -xzf $HOME/tmp/hmmer.tar.gz -C $HOME/tmp
    cd $HOME/tmp/hmmer-*
    ./configure --prefix=$HOME/.local
    make
    make install
    export PATH=$HOME/.local/bin:$PATH
    echo 'export PATH=$HOME/.local/bin:$PATH' >> ~/.bashrc
    source ~/.bashrc
    condition=1
else
    echo "hmmsearch is already installed"
fi

# Install jq if not found
if ! command -v jq &> /dev/null
then
    echo "jq could not be found, installing..."
    mkdir -p $HOME/tmp
    wget -O $HOME/tmp/jq https://stedolan.github.io/jq/download/linux64/jq
    chmod +x $HOME/tmp/jq
    mv $HOME/tmp/jq $HOME/.local/bin/jq
    export PATH=$HOME/.local/bin:$PATH
    echo 'export PATH=$HOME/.local/bin:$PATH' >> ~/.bashrc
    source ~/.bashrc
    condition=1
else
    echo "jq is already installed"
fi

# Install PhasTest_API if not found
if [ ! -f "$HOME/.local/bin/phastest_api.sh" ]; then
    echo "PhasTest_API could not be found, installing..."
    mkdir -p $HOME/.local/bin
    wget https://github.com/ansontwk/PhasTest_API/raw/main/phastest_api.sh -O $HOME/.local/bin/phastest_api.sh
    chmod +x $HOME/.local/bin/phastest_api.sh
    condition=1
else
    echo "PhasTest_API is already installed"
fi

# Initialize conda if not already done
if ! grep -q 'conda initialize' ~/.bashrc; then
    conda init
    source ~/.bashrc
fi

# Create and activate defensefinder environment
if ! conda env list | grep -q 'defensefinder'; then
    echo "defense-finder could not be found, installing..."
    pip install colorlog
    conda create --name defensefinder -c bioconda -c conda-forge defense-finder -y
    condition = 1
else
    echo "defense-finder is already installed"
fi

# Create genomad environment if not found
if ! conda env list | grep -q 'genomad'; then
    echo "genomad could not be found, installing..."
    conda create -n genomad -c conda-forge -c bioconda genomad -y
    condition = 1
else
    echo "genomad is already installed"
fi


source ~/.bashrc
if [ $condition -eq 1 ]
then
    echo -e "\e[32mAll dependencies have been installed successfully\e[0m"
    echo -e "\e[33m###############################################\e[0m"
    echo -e "\e[33m# Please restart your terminal to use the     #\e[0m"
    echo -e "\e[33m# installed tools                             #\e[0m"
    echo -e "\e[33m###############################################\e[0m"
    echo ""
    echo -e "\e[34mThen, run 'python run.py --help' to see the available options\e[0m"
else 
    echo -e "\e[32mAll dependencies are already installed\e[0m"
    echo -e "\e[34mYou can now run 'python run.py --help' to see the available options\e[0m"
fi

echo ""

