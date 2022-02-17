from scipy.stats import pearsonr
import argparse
from util import parse_sts
from nltk.translate.nist_score import sentence_nist
from nltk.translate.bleu_score import sentence_bleu
from nltk import word_tokenize, edit_distance
from difflib import SequenceMatcher
import warnings
warnings.filterwarnings("ignore")


def main(sts_data):
    """Calculate pearson correlation between semantic similarity scores and string similarity metrics.
    Data is formatted as in the STS benchmark"""

    # TODO 1: read the dataset; implement in util.py
    texts, labels = parse_sts(sts_data)

    print(f"Found {len(texts)} STS pairs")

    # TODO 2: Calculate each of the the metrics here for each text pair in the dataset
    # HINT: Longest common substring can be complicated. Investigate difflib.SequenceMatcher for a good option.
    score_types = ["NIST", "BLEU", "Word Error Rate", "Longest common substring", "Edit Distance"]

    nist_scores = []
    bleu_scores = []
    wer_scores = []
    lcs_scores = []
    ed_scores = []

    for text in texts:
        t1, t2 = text
        # tokenize the sentences
        t1_toks = word_tokenize(t1.lower())
        t2_toks = word_tokenize(t2.lower())

        # nist score
        try:
            nist_1 = sentence_nist([t1_toks, ], t2_toks)
        except ZeroDivisionError:
            nist_1 = 0.0

        try:
            nist_2 = sentence_nist([t2_toks, ], t1_toks)
        except ZeroDivisionError:
            nist_2 = 0.0

        nist_score = nist_1 + nist_2
        nist_scores.append(nist_score)

        # bleu
        try:
            bleu_1 = sentence_bleu([t1_toks, ], t2_toks, smoothing_function=None)
        except ZeroDivisionError:
            bleu_1 = 0.0

        try:
            bleu_2 = sentence_bleu([t2_toks, ], t1_toks, smoothing_function=None)
        except ZeroDivisionError:
            bleu_2 = 0.0

        bleu_score = bleu_1 + bleu_2

        bleu_scores.append(bleu_score)
        # Word error rate
        wer_1 = edit_distance(t1_toks, t2_toks) / max(len(t1_toks), len(t2_toks))
        wer_2 = edit_distance(t2_toks, t1_toks) / min(len(t1_toks), len(t2_toks))
        wer_score = wer_1 + wer_2
        wer_scores.append(wer_score)

        # Longest Common Distance
        seq = SequenceMatcher(None, t1, t2)
        match = seq.find_longest_match(0, len(t1), 0, len(t2))
        lcs = match.size

        lcs_scores.append(lcs)
        # Edit Distance
        ed_scores.append(edit_distance(t1, t2))

    metrics = dict(zip(score_types, [nist_scores, bleu_scores, wer_scores, lcs_scores, ed_scores]))

    #TODO 3: Calculate pearson r between each metric and the STS labels and report in the README.
    # Sample code to print results. You can alter the printing as you see fit. It is most important to put the results
    # in a table in the README
    print(f"Semantic textual similarity for {sts_data}\n")
    for metric_name in score_types:
        score = pearsonr(metrics[metric_name], labels)[0]
        print(f"{metric_name} correlation: {score:.03f}")

    # TODO 4: Complete writeup as specified by TODOs in README (describe metrics; show usage)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sts_data", type=str, default="stsbenchmark/sts-dev.csv",
                        help="tab separated sts data in benchmark format")
    args = parser.parse_args()

    main(args.sts_data)

