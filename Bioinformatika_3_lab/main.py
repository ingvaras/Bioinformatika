import matplotlib.pyplot as plt
from bioinfokit.analys import fastq
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML

formats = dict({
    'Sanger Phred+33': (33, 73),
    'Solexa Solexa+64': (59, 104),
    'Illumina 1.3+ Phred+64': (64, 104),
    'Illumina 1.5+ Phred+64': (67, 105),
    'Illumina 1.8+ Phred+33': (33, 74),
})


def blast_search(seq):
    result_handle = NCBIWWW.qblast("blastn", "nt", seq, alignments=1, hitlist_size=1)
    records = NCBIXML.parse(result_handle)
    for rec in records:
        for alignment in rec.alignments:
            return alignment.hit_def


if __name__ == '__main__':
    fastq_iterator = fastq.fastq_reader(file='resources/reads_for_analysis.fastq')

    quality_score_concatenation = ""
    gc_ratios = []

    ids = []
    sequences = []

    for entry in fastq_iterator:
        seq_id, sequence, _, quality_score = entry
        quality_score_concatenation = quality_score_concatenation + quality_score
        gc_ratios.append(round((sequence.count('G') + sequence.count('C')) / len(sequence), 2))
        ids.append(seq_id)
        sequences.append(sequence)
    unique_characters = set(quality_score_concatenation)

    # a)
    for format in formats:
        characters_are_in_encoding_range = True
        for character in unique_characters:
            if ord(character) < formats[format][0] or ord(character) > formats[format][1]:
                characters_are_in_encoding_range = False
        if characters_are_in_encoding_range:
            print(format)

    # b)
    x_axis = []
    y_axis = []
    for i in range(0, 100):
        x_axis.append(i / 100)
    for x in x_axis:
        y_axis.append(gc_ratios.count(x))
    plt.plot(x_axis, y_axis)
    plt.xlabel('C/G nukleotidų dalis')
    plt.ylabel('read’ų skaičius')
    plt.show()

    # c)
    # Peak 1: 0.34
    print(x_axis[y_axis[:40].index(max(y_axis[:40]))])
    # Peak 2: 0.54
    print(x_axis[40:60][y_axis[40:60].index(max(y_axis[40:60]))])
    # Peak 3: 0.70
    print(x_axis[60:][y_axis[60:].index(max(y_axis[60:]))])

    peak_1_ids = []
    peak_1_sequences = []
    peak_2_ids = []
    peak_2_sequences = []
    peak_3_ids = []
    peak_3_sequences = []
    peak_1_positions = [j for j, x in enumerate(gc_ratios) if x == 0.34][:5]
    peak_2_positions = [j for j, x in enumerate(gc_ratios) if x == 0.54][:5]
    peak_3_positions = [j for j, x in enumerate(gc_ratios) if x == 0.7][:5]
    for position in peak_1_positions:
        peak_1_ids.append(ids[position])
        peak_1_sequences.append(sequences[position])
    for position in peak_2_positions:
        peak_2_ids.append(ids[position])
        peak_2_sequences.append(sequences[position])
    for position in peak_3_positions:
        peak_3_ids.append(ids[position])
        peak_3_sequences.append(sequences[position])
    print(peak_1_sequences)
    print(peak_2_sequences)
    print(peak_3_sequences)

    ids_column = []
    bacteria_column = []
    for seq_id in peak_1_ids:
        ids_column.append(seq_id)
    for seq_id in peak_2_ids:
        ids_column.append(seq_id)
    for seq_id in peak_3_ids:
        ids_column.append(seq_id)

    for s in peak_1_sequences:
        bacteria_column.append(blast_search(s))
    for s in peak_2_sequences:
        bacteria_column.append(blast_search(s))
    for s in peak_3_sequences:
        bacteria_column.append(blast_search(s))

    print(ids_column)
    print(bacteria_column)
