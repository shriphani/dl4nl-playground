'''
PTB Dataset
'''

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

if __name__ == '__main__':
    tagset = load_tagset()
    data = []
    data_dir = '../data/eng_news_txt_tbnk-ptb_revised/data/penntree/'
    for root, dirs, files in os.walk(data_dir):
        for filename in files:
            if filename.find('wsj') < 0:
                continue

            file_path = os.path.join(
                root,
                filename
            )

            file_data = process_file(file_path, tagset)

            for sequence in file_data:
                for tag, tok in sequence:
                    print tag, tok
                print
