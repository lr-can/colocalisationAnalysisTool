#!/bin/bash
export PATH=.venv/:$PATH

# Install HMMER if not found
if ! command -v hmmsearch &> /dev/null
then
    echo "hmmsearch could not be found, installing..."
    wget http://eddylab.org/software/hmmer/hmmer.tar.gz -O /tmp/hmmer.tar.gz
    tar -xzf /tmp/hmmer.tar.gz -C /tmp
    cd /tmp/hmmer-*
    ./configure --prefix=$HOME/hmmer
    make
    make install
    export PATH=$HOME/hmmer/bin:$PATH
    echo 'export PATH=$HOME/hmmer/bin:$PATH' >> ~/.bashrc
    source ~/.bashrc
else
    echo "hmmsearch is already installed"
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
else
    echo "defense-finder is already installed"
fi

# Create genomad environment if not found
if ! conda env list | grep -q 'genomad'; then
    echo "genomad could not be found, installing..."
    conda create -n genomad -c conda-forge -c bioconda genomad -y
else
    echo "genomad is already installed"
fi


source ~/.bashrc
echo "All dependencies have been installed successfully"
