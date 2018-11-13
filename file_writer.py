import csv
import os
from specgram_maker import SpecgramMaker
from Regression import Regression


def write_row_data_excl(filepath, rows):
    with open(filepath, "w", newline="\n") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        x=1
        for row in rows:
            print("Writing row: " + str(x))
            x += 1
            writer.writerow(row)


# Generates metadata for arff type dataset
def _arff_metadata(title, num_labels, class1, class2, label_type = "REAL"):
    metadata = []
    # a1, a2, .., a_n label
    metadata.extend([["@RELATION {}".format(title)]])
    for x in range(num_labels):
        metadata.extend([["@ATTRIBUTE a{} ".format(str(x)) + label_type]])
    metadata.extend([["@ATTRIBUTE class {{{}".format(class1), "{}}}".format(class2)]])
    metadata.extend([["@DATA"]])
    return metadata


def extract_frequency_data(siren_dir, no_siren_dir, out, max_freq = 442):
    e = Regression()
    g = []

    # extracting siren frequencies
    print("Extracting siren spectrograms")
    f, t = e.extract(siren_dir, max_freq)
    f1, t = e.extract(siren_dir, 40)

    g.extend(_arff_metadata("siren", len(f[0]*2), "siren", "nosiren"))

    for x in range(len(f)):
        g_list = []
        g_list.extend(f[x])
        g_list.extend(f1[x])
        g_list.append("siren")
        g.append(g_list)

    print("Extracting nosiren spectrograms")
    f, t = e.extract(no_siren_dir)
    f1, t = e.extract(no_siren_dir, 40)

    for x in range(len(f)):
        g_list = []
        g_list.extend(f[x])
        g_list.extend(f1[x])
        g_list.append("nosiren")
        g.append(g_list)
    write_row_data_excl(out, g)


def matrices_from_dir(path):
    matrices = []
    directory = os.listdir(path)
    sm = SpecgramMaker()
    for filename in directory:
        print("Extracting data from " + filename)
        if not filename.endswith(".wav"):
            continue
        spec, freq, t = sm.get_specgram_data_from_wav(path, filename)
        matrices.append(spec)
    return matrices


def get_matrix_data(siren_dir, no_siren_dir, out):
    ns_matrices = matrices_from_dir(no_siren_dir)
    s_matrices = matrices_from_dir(siren_dir)
    data_set = []

    ns_row_length = len(ns_matrices[0])
    ns_col_length = len(ns_matrices[0][0])

    s_row_length = len(s_matrices[0])
    s_col_length = len(s_matrices[0][0])

    if ns_row_length != s_row_length or ns_col_length != s_col_length:
        print("Data conversion ERROR: Datasets are not same size")
        exit(-1)

    data_set.extend(_arff_metadata("siren", ns_row_length * ns_col_length, "siren", "nosiren"))

    for matrix in s_matrices:
        data_set.append(_extract_data_row(matrix, "siren"))

    for matrix in ns_matrices:
        data_set.append(_extract_data_row(matrix, "nosiren"))

    write_row_data_excl(out, data_set)


def _extract_data_row(matrix, label):
    cell_list = []
    for row in matrix:
        cell_list += row.tolist()
    cell_list.append(label)
    return cell_list


if __name__ == '__main__':
    output_filename = "cmf_teesthøj3_50_50_1000.arff"
    s_dir = "C:\\Users\\kristoffer\\Desktop\\teesthøj3_50_50_1000\\siren\\"
    ns_dir = "C:\\Users\\kristoffer\\Desktop\\teesthøj3_50_50_1000\\nosiren\\"
    extract_frequency_data(s_dir, ns_dir, output_filename)
    # extract_data_csv(siren_dir, nosiren_dir, output_filename)
