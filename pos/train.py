'''
Train a character model
'''

from ptb_data import load_tagset
import numpy as np
import sys
import tensorflow as tf

SEQ_LEN = 1000 # 10k chars in a sentence
BATCH_SIZE = 128
HIDDEN_UNITS = 100

def load_sequences(ptb_filename):
    with open(ptb_filename, 'r') as handle:
        sequences = []
        cur_seq = []
        for new_line in handle:
            new_line = new_line.strip()
            if new_line == '':
                sequences.append(cur_seq)
                cur_seq = []

            else:
                cur_seq.append(new_line)

        return sequences

def get_char_maps(seqs):
    char2idx = {}
    idx2char = {}

    chars = set([])

    for seq in seqs:
        for tagged_word in seqs:
            tag, word = tagged_word.split()
            for char in word:
                chars.add(char)

    char_list = list(chars)
    char_list.sort()

    for i, c in enumerate(char_list):
        char2idx[c] = i
        idx2char[i] = c

    return char2idx, idx2char

def setup_char_model(char_model, tagset):

    # the input is a set of one-hot vectors for characters
    input_data = tf.placeholder(
        tf.bool,
        shape=(
            BATCH_SIZE,
            SEQ_LEN,
            len(tagset)
        )
    )

    # the output is a probability vector w/ the prob.
    # of each char having a particular tag.

def seq2one_hot(seq, char2idx, idx2char):
    '''
    Convert a sequence into a one-hot vector
    '''
    result = []
    for tagged_word in seq:

        tagged_word = tagged_word.strip()
        tag, word = tagged_word.split()
        for char in word:
            vector = np.zeros((len(char2idx)), dtype=np.bool)
            vector[char2idx[char]] = 1

            result.append(vector)

    return result

if __name__ == '__main__':
    train_file = sys.argv[1]
    val_file = sys.argv[2]
    test_file = sys.argv[3]

    tagset = load_tagset()

    train_seqs = load_sequences(train_file)
    val_seqs = load_sequences(val_file)
    test_seqs = load_sequences(test_file)

    char2idx, idx2char = get_char_maps(train_seqs + val_seqs + test_seqs)

    for seq in train_seqs:
        print seq2one_hot(seq, char2idx, idx2char)
