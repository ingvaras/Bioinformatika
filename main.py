import math
from Bio import SeqIO
from Bio.Seq import Seq

species = ["B1", "B2", "B3", "B4", "M1", "M2", "M3", "M4"]
codons = "ARNDCEQGHILKMFPSTWYV"


def distance_function(a, b):
    return math.pow((a - b), 2)


def extract_all_three_possible_sequences(sequence):
    sequences = []
    for i in range(0, 3):
        sequences.append([sequence.seq[(j + i) * 3:(j + i) * 3 + 3] for j in range(len(sequence.seq) // 3)])
    return sequences


# 1, 2, 3 tasks
def find_and_filter_coding_sequences(filename):
    sequences = []
    for seq in SeqIO.parse("resources/" + filename, "fasta"):
        for j in range(0, 3):
            if len(seq.seq[j:]) % 3 != 0:
                sequence = Seq(seq.seq[j:-(len(seq.seq[j:]) % 3)])
                sequences.append(sequence)
                sequences.append(sequence.reverse_complement())
            else:
                sequence = Seq(seq.seq[j:])
                sequences.append(sequence)
                sequences.append(sequence.reverse_complement())
    coding_sequences = []
    for sequence in sequences:
        last_stop_index = 0
        for k in range(0, len(sequence), 3):
            if k < last_stop_index:
                continue
            if sequence[k:k + 3] == 'ATG':
                for j in range(k, len(sequence), 3):
                    if sequence[j:j + 3] == 'TAA' or sequence[j:j + 3] == 'TAG' or sequence[j:j + 3] == 'TGA':
                        if j + 3 - k >= 100:
                            coding_sequences.append(sequence[k:j + 3].translate())
                        last_stop_index = j + 3
                        break
    return coding_sequences


def calculate_codon_frequencies(sequences):
    codon_frequencies = []
    for codon in codons:
        counter = 0
        sequences_length = 0
        for sequence in sequences:
            sequences_length += len(sequence)
            for k in range(len(sequence)):
                if sequence[k] == codon:
                    counter += 1
        codon_frequencies.append(counter / sequences_length)
    return codon_frequencies


def calculate_dicodon_frequencies(sequences):
    dicodon_frequencies = []
    for first_codon in codons:
        for second_codon in codons:
            counter = 0
            sequences_length = 0
            for sequence in sequences:
                sequences_length += len(sequence)
                for k in range(len(sequence) - 1):
                    if sequence[k] == first_codon and sequence[k + 1] == second_codon:
                        counter += 1
            dicodon_frequencies.append(counter / sequences_length)
    return dicodon_frequencies


def create_distance_matrix(frequencies):
    matrix = [[0.0 for _ in range(8)] for _ in range(8)]
    for i in range(0, len(frequencies) - 1):
        for j in range(i + 1, len(frequencies)):
            counter = 0.0
            for k in range(len(frequencies[i])):
                counter += distance_function(frequencies[i][k], frequencies[j][k])
            matrix[i][j] = math.sqrt(counter)
            matrix[j][i] = matrix[i][j]
    return matrix


if __name__ == '__main__':
    codon_frequencies = []
    dicodon_frequencies = []

    for i in range(1, 5):
        coding_sequences = find_and_filter_coding_sequences("bacterial" + str(i) + ".fasta")
        codon_frequencies.append(calculate_codon_frequencies(coding_sequences))
        dicodon_frequencies.append(calculate_dicodon_frequencies(coding_sequences))
    for i in range(1, 5):
        coding_sequences = find_and_filter_coding_sequences("mamalian" + str(i) + ".fasta")
        codon_frequencies.append(calculate_codon_frequencies(coding_sequences))
        dicodon_frequencies.append(calculate_dicodon_frequencies(coding_sequences))

    print("B1 B2 B3 B4 M1 M2 M3 M4")
    codon_distance_matrix = create_distance_matrix(codon_frequencies)
    for distance in codon_distance_matrix:
        print(distance)

    print("B1 B2 B3 B4 M1 M2 M3 M4")
    dicodon_distance_matrix = create_distance_matrix(dicodon_frequencies)
    for distance in dicodon_distance_matrix:
        print(distance)

    # Phylip format
    print(len(codon_distance_matrix))
    for distance_list in codon_distance_matrix:
        print(species[codon_distance_matrix.index(distance_list)], end=" ")
        for distance in distance_list:
            print(distance, end=" ")
        print()

    print(len(dicodon_distance_matrix))
    for distance_list in dicodon_distance_matrix:
        print(species[dicodon_distance_matrix.index(distance_list)], end=" ")
        for distance in distance_list:
            print(distance, end=" ")
        print()