import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Script to check file.")
    parser.add_argument('-file', type=str, required=True, help="Path to the file to be checked.")
    return parser.parse_args()

class Fasta_sequence:
    """
    Class to store a fasta sequence.
    """
    def __init__(self, header, sequence):
        self.header = header
        self.sequence = sequence

    def __str__(self):
        return f">{self.header}\n{self.sequence}"
    
    def verif_if_dna(self):
        """
        Check if the sequence is a DNA sequence.
        """
        dna = set('ATCGN')
        return set(self.sequence.upper()).issubset(dna)

import gzip

def read_fasta(file_):
    if file_.endswith('.gz'):
        open_func = gzip.open
        mode = 'rt'
    else:
        open_func = open
        mode = 'r+'
    with open_func(file_, mode) as f:
        fasta_sequences = []
        file_content = f.read()
        entries = file_content.strip().split('>')
        for entry in entries:
            if entry:
                lines = entry.split('\n')
                header = lines[0]
                sequence = ''.join(lines[1:])
                fasta_sequences.append(Fasta_sequence(header, sequence))
        print("\033[96mchecking if the file contains only dna sequences\033[0m")
        for fasta_sequence in fasta_sequences:
            if not fasta_sequence.verif_if_dna():
                raise ValueError(f"The sequence {fasta_sequence.header} is not a DNA sequence.")
            print("\033[92mAll sequences are DNA sequences.\033[0m")

        print("\033[96mChecking and removing duplicate sequences\033[0m")
        unique_sequences = {}
        condition = False
        for fasta_sequence in fasta_sequences:
            if fasta_sequence.header not in unique_sequences:
                unique_sequences[fasta_sequence.header] = fasta_sequence
            else:
                print(f"\033[93mDuplicate found: {fasta_sequence.header}\033[0m")
                condition = True
        if not condition:
            print("\033[92mNo duplicates found.\033[0m")
            return
        fasta_sequences = list(unique_sequences.values())
        print(f"\033[92mDuplicates removed. Remaining unique sequences count : {len(fasta_sequences)}\033[0m")
        buffer_fasta_file = ""
        for fasta_sequence in fasta_sequences:
            buffer_fasta_file += str(fasta_sequence) + "\n"
        f.seek(0)
        f.write(buffer_fasta_file)
        f.truncate()
        print("\033[92mFile cleaned.\033[0m")

if __name__ == "__main__":
    args = parse_arguments()
    read_fasta(args.file)
            
