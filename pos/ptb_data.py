'''
PTB Dataset
'''

from numpy.random import uniform
from sexpdata import loads, dumps, Symbol
import os
import sys

def load_tagset(filename='../data/tagset.txt'):
    tags = []
    with open(filename) as handle:
        for new_line in handle:
            pos_tag = new_line.split()[0]
            tags.append(pos_tag)

    return set(tags)

def is_leaf(a_tree):
    return not isinstance(a_tree, list)

def is_pos_tag(label, tagset):
    return label in tagset

def get_label(a_leaf):
    if isinstance(a_leaf, Symbol):
        return a_leaf.value()
    else:
        return a_leaf

def is_penultimate(a_tree):
    return len(a_tree) == 2 and not isinstance(a_tree[1], list)

def process_tree(a_tree, tagset):
    if isinstance(a_tree, Symbol):
        return []
    node_label = a_tree[0].value()
    if is_pos_tag(node_label, tagset):
        return [(node_label, get_label(a_tree[1]))]
    elif is_penultimate(a_tree):
        return [('UNK', get_label(a_tree[1]))]
    else:
        tags = []
        for tree in a_tree[1:]:
            tags.extend(process_tree(tree, tagset))
        return tags

def process_s_expr(s_expr_str, tagset):
    return process_tree(
        loads(
            s_expr_str
        )[0],
        tagset
    )

def process_file(a_file, tagset):
    file_data = []
    with open(a_file) as handle:
        for new_line in handle:
            try:
                file_data.append(
                    process_s_expr(
                        new_line.strip(),
                        tagset
                    )
                )
            except:
                pass
    return file_data

def split(ptb_filename, train=70, validation=20):
    '''
    Split the dataset.
    '''
    sequences = []
    cur_seq = []
    with open(ptb_filename, 'r') as handle:
        for new_line in handle:
            new_line = new_line.strip()
            if new_line == '':
                sequences.append(cur_seq)
                cur_seq = []

            else:
                cur_seq.append(new_line)

    train_seqs = []
    validation_seqs = []
    test_seqs = []

    for seq in sequences:
        sample = uniform()

        if sample < 0.1:
            validation_seqs.append(seq)

        elif sample < 0.3:
            test_seqs.append(seq)

        else:
            train_seqs.append(seq)

    return train_seqs, validation_seqs, test_seqs

if __name__ == '__main__':
    data = sys.argv[1]
    train, val, test = split(data)

    print 'train:', len(train), 'validation:', len(val), 'test:', len(test)

    with open('ptb_pos_train.txt', 'w') as train_handle:
        for seq in train:
            for line in seq:
                train_handle.write(line + '\n')
            train_handle.write('\n')

    with open('ptb_pos_val.txt', 'w') as val_handle:
        for seq in val:
            for line in seq:
                val_handle.write(line + '\n')
            val_handle.write('\n')

    with open('ptb_pos_test.txt', 'w') as test_handle:
        for seq in test:
            for line in seq:
                test_handle.write(line + '\n')
            test_handle.write('\n')
