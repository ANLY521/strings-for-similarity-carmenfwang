# TODO: lab, homework
import codecs

def parse_sts(data_file):
    """
    Reads a tab-separated sts benchmark file and returns
    texts: list of tuples (text1, text2)
    labels: list of floats
    """
    texts = []
    labels = []

    with codecs.open(data_file, "r", "utf-8") as df:
        for line in df:
            fields = line.strip().split("\t")
            labels.append(float(fields[4])) # the score
            t1 = fields[5].lower()
            t2 = fields[6].lower()
            texts.append((t1, t2))
    return texts, labels