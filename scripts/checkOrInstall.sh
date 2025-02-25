#!/bin/bash
export PATH=.venv/:$PATH
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

if ! command -v defense-finder &> /dev/null
then
    echo "defense-finder could not be found, installing..."
    if [ ! -f ./requirements.txt ]; then
        echo "requirements.txt not found, creating a default one..."
        echo "mdmparis-defense-finder" > ./requirements.txt
    fi
    pip install -r ./requirements.txt --target .venv
    pip install numpy==1.26.0 --target .venv
else
    echo "defense-finder is already installed"
fi

#if ! command -v mmseqs &> /dev/null
#then
#    echo "mmseqs could not be found, installing..."
#    wget https://mmseqs.com/latest/mmseqs-linux-avx2.tar.gz -O /tmp/mmseqs.tar.gz
#   tar -xzf /tmp/mmseqs.tar.gz -C /tmp
#    mkdir -p $HOME/bin
#    mv /tmp/mmseqs/bin/* $HOME/bin/
#    export PATH=$HOME/bin:$PATH
#    echo 'export PATH=$HOME/bin:$PATH' >> ~/.bashrc
#    source ~/.bashrc
#    echo "mmseqs installed successfully"
#else
#    echo "mmseqs is already installed"
#fi

#if ! command -v aragorn &> /dev/null
#then
#    echo "aragorn could not be found, installing..."
#    mkdir -p $HOME/bin
#    gcc /tmp/aragorn.c -o $HOME/bin/aragorn
#    gcc /tmp/aragorn.c -o $HOME/bin/aragorn
#    export PATH=$HOME/bin:$PATH
#    echo 'export PATH=$HOME/bin:$PATH' >> ~/.bashrc
#    source ~/.bashrc
#else
#    echo "aragorn is already installed"
#fi

#if ! command -v genomad &> /dev/null
#then
#    echo "genomad could not be found, installing..."
#    pip install genomad --target .venv
mkdir -p ./.venv/bin
cp -r ./.venv/bin/* ./.venv/
#    echo "genomad is already installed"
#fi


source ~/.bashrc
echo "All dependencies have been installed successfully"