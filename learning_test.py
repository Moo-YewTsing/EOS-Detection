import pickle
import random
import os
from os.path import join, splitext
from collections import defaultdict
import sys
from Unet_box.EOS_tools import get_name

def from_names_to_path_list(names:list, tiles_dir:str) -> dict:
    """collect the path of tiles by their parents' file names"""
    parents = set(names)
    container1 = {}
    container2 = {}
    
    for kind in ('labels', 'raw_imgs'):
        directory = join(tiles_dir, kind)
        collector1 = defaultdict(list)
        collector2 = defaultdict(list)
        for fn in os.listdir(directory):
            parent = fn.rsplit('_', 1)[0]
            if parent in parents:
                collector1[parent].append(join(tiles_dir, fn))
            else:
                collector2[parent].append(join(tiles_dir, fn))
        container1[kind] = collector1
        container2[kind] = collector2
    return container1, container2

def save_dict(container:dict, name, dst) -> None:
    os.makedirs(dst, exist_ok=True)
    with open(join(dst, name+'.pkl'), 'wb+') as saver:
        pickle.dump(container, saver, pickle.HIGHEST_PROTOCOL)

def names_separator(all_names:list, percent=0.2) -> list:
    random.seed(42)
    amount = len(all_names)
    number = int(percent * amount)
    # temp = all_names[:]
    # random.shuffle(temp)
    # part = temp[:number]
    # left = temp[number:]
    part = random.sample(all_names, number)
    return part

def names_creator(dir_path):
    return [get_name(fn) for fn in os.listdir(dir_path)]

def train_test_info_creator(label_dir, tiles_dir, dst):
    all_names = names_creator(label_dir)
    test_names = names_separator(all_names)
    test_family, other_family = from_names_to_path_list(test_names, tiles_dir)
    save_dict(test_family, 'test', dst)
    save_dict(other_family, 'others', dst)

if __name__ == "__main__":
    label_dir = sys.argv[1]
    tiles_dir = sys.argv[2]
    dst = sys.argv[3]
    train_test_info_creator(label_dir, tiles_dir, dst)
