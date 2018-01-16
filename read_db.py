#!/usr/bin/env python
# -*- coding: utf-8 -*-


import time
import argparse
from pymongo import MongoClient
import re
import numpy as np



def read_db():
    client = MongoClient('localhost', 27017) # 第2引数はポート番号
    collection = client.scraping.paper       # scraping データベースの paper コレクションを得る

    titles = []
    abstracts = []
    for entry in collection.find():
        titles.append(re.sub('\s+', ' ', entry['Title']).replace('\n', ''))
        abstracts.append(re.sub('\s+', ' ', entry['Abstract']).replace('\n', ''))
        #print('-' * 80)
        #time.sleep(1)
    return titles, abstracts


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='read_db',
                                     usage='read DB and output train text',
                                     add_help=True, # -h/?help オプションの追加
    )
    parser.add_argument('--train_src', type=str, default='train_src.txt')
    parser.add_argument('--train_tgt', type=str, default='train_tgt.txt')
    parser.add_argument('--test_src', type=str, default='test_src.txt')
    parser.add_argument('--test_tgt', type=str, default='test_tgt.txt')
    parser.add_argument('--n_train', type=int, default=10000)
    args = parser.parse_args()

    titles, abstracts = read_db()

    idx = np.random.permutation(len(titles))

    f_src = open(args.train_src, 'w')
    f_tgt = open(args.train_tgt, 'w')
    for i in idx[:args.n_train]:
        f_src.write(abstracts[i] + '\n')
        f_tgt.write(titles[i] + '\n')
    f_src.close()
    f_tgt.close()

    f_src = open(args.test_src, 'w')
    f_tgt = open(args.test_tgt, 'w')
    for i in idx[args.n_train:]:
        f_src.write(abstracts[i] + '\n')
        f_tgt.write(titles[i] + '\n')
    f_src.close()
    f_tgt.close()

    
