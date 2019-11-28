import pickle
import collections
import sys
import time
from tqdm import tqdm
import operator


def tokenize(string):
    out = string.split(' ')
    return out

def count_ngrams(line):
    queue = collections.deque(maxlen=max_length)

    # Helper function to add n-grams at start of current queue to dict
    def add_queue():
        current = tuple(queue)
        for length in lengths:
            if len(current) >= length:
                ngrams[length][current[:length]] += 1

    # Loop through all lines and words and add n-grams to dict
    for word in tokenize(line):
        queue.append(word)
        if len(queue) >= max_length:
            add_queue()

    # Make sure we get the n-grams at the tail end of the queue
    while len(queue) > min_length:
        queue.popleft()
        add_queue()


def print_most_frequent(ngrams, num=3):
    """Print num most common n-grams of each length in n-grams dict."""
    for n in sorted(ngrams):
        print('----- {} most common {}-grams -----'.format(num, n))
        for gram, count in ngrams[n].most_common(num):
            print('{0}: {1}'.format(' '.join(gram), count))
        print()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python ngrams.py filename')
        sys.exit(1)

    min_length = 1
    max_length = 3
    lengths = range(min_length, max_length + 1)
    ngrams = {length: collections.Counter() for length in lengths}

    start_time = time.time()
    #for i, file in enumerate(os.listdir('/home/kraken/jakub.pokrywka/NER/LM_no_diacritics_lower')):
    with open(sys.argv[1]) as f:
        for line in tqdm(f):
            count_ngrams(line.rstrip('\n'))
    print_most_frequent(ngrams)
    elapsed_time = time.time() - start_time
    print('Took {:.03f} seconds'.format(elapsed_time))

    pickle.dump(ngrams, open(sys.argv[2], 'wb'))

