import csv
import clip_split as cs


def _write_row_data_excl(filepath, rows):
    with open(filepath, "w", newline="\n") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        x = 1
        for row in rows:
            print("Writing row: " + str(x))
            x += 1
            writer.writerow(row)


# Generates metadata for arff type dataset
def _arff_metadata(title, num_features, class1, class2, label_type = "REAL"):
    metadata = []
    # a1, a2, .., a_n label
    metadata.extend([["@RELATION {}".format(title)]])
    for x in range(num_features):
        metadata.extend([["@ATTRIBUTE a{} ".format(str(x)) + label_type]])
    metadata.extend([["@ATTRIBUTE class {{{}".format(class1), "{}}}".format(class2)]])
    metadata.extend([["@DATA"]])
    return metadata


def get_ver_max_data(data_dir, out, divisions=1):
    # setup
    g = []

    # extracting features
    print("Extracting features")
    freq, time, lab = cs.extract(data_dir, divisions=divisions)
    g.extend(_arff_metadata("sirendata", len(freq[0]), "siren", "nosiren"))

    for x in range(len(freq)):
        g_list = []
        g_list.extend(freq[x])
        if lab[x]:
            g_list.append("siren")
        else:
            g_list.append("nosiren")
        g.append(g_list)
    _write_row_data_excl(out, g)


if __name__ == '__main__':
    output_filename = "testtest.arff"
    dir = "C:\\Users\\kristoffer\\Desktop\\Skrivebord\\training_data\\teest\\"
    # To extract data with 5 splits
    get_ver_max_data(dir, output_filename, 5)
