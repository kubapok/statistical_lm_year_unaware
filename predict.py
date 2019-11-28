import sys
import pickle
from tqdm import tqdm
import numpy as np

log = np.log

in_f = open(sys.argv[1], 'r')
out_f = open(sys.argv[2], 'w')

ngrams_dict = pickle.load(open('./data/ngrams.pickle', 'rb'))

UNIGRAMS_OUT_NUMBER = 100
BIGRAMS_OUT_NUMBER = 80
TRIGRAMS_OUT_NUMBER = 80

MIN_BIGRAMS_COUNT = 20
MIN_TRIGRAMS_NUMBER = 20


def _get_unigrams(return_number):
    n_sorted = sorted(tuple((ngrams_dict[1][x], x) for x in ngrams_dict[1]), reverse=True)
    ngrams_sum = sum([x[0] for x in n_sorted])
    out = [x[1][0] + ':' + str(log(x[0] / ngrams_sum)) for x in n_sorted[:return_number - 1]]
    out = out + [':' + str(log(1 - sum([(x[0] / ngrams_sum) for x in n_sorted[return_number - 1:return_number]])))]
    return ' '.join(out)


unigrams = _get_unigrams(UNIGRAMS_OUT_NUMBER)


def get_bigrams(return_number, token_before):
    n_sorted = sorted(tuple((ngrams_dict[2][x], x) for x in ngrams_dict[2] if x[0] == token_before), reverse=True)
    ngrams_sum = sum([x[0] for x in n_sorted])
    if ngrams_sum < MIN_BIGRAMS_COUNT:
        return False
    elif len(n_sorted) < return_number:
        ngrams_sum *= 2
    out = [x[1][1] + ':' + str(log(x[0] / ngrams_sum)) for x in n_sorted[:return_number - 1]]
    out = out + [':' + str(log(1 - sum([(x[0] / ngrams_sum) for x in n_sorted[:return_number - 1]])))]
    return ' '.join(out)


def get_trigrams(return_number, token_before, token_after):
    n_sorted = sorted(tuple((ngrams_dict[3][x], x) for x in ngrams_dict[3] if x[0] == token_before and x[2] == token_after), reverse=True)
    ngrams_sum = sum([x[0] for x in n_sorted])
    if ngrams_sum < MIN_TRIGRAMS_NUMBER:
        return False
    elif len(n_sorted) < return_number:
        ngrams_sum *= 2
    out = [x[1][1] + ':' + str(log(x[0] / ngrams_sum)) for x in n_sorted[:return_number - 1]]
    out = out + [':' + str(log(1 - sum([(x[0] / ngrams_sum) for x in n_sorted[:return_number - 1]])))]
    return ' '.join(out)


def get_words_and_scores(line):
    _, _, text_before, text_after = line.split('\t')

    tokens_before = text_before.split()[-1:][0]
    tokens_after = text_after.split()[:1][0]

    output = get_trigrams(TRIGRAMS_OUT_NUMBER, tokens_before, tokens_after)
    if not output:
        output = get_bigrams(BIGRAMS_OUT_NUMBER, tokens_before)
        if not output:
            output = unigrams
    return output


for line in tqdm(in_f):
    out = get_words_and_scores(line) + '\n'
    out_f.write(out)
    print(get_words_and_scores(line))
