#!/usr/bin/env python
# -*- coding: utf-8 -*-


import time
import argparse
from pymongo import MongoClient
import re
import numpy as np



def read_db():
    client = MongoClient('mongo', 27017) # 第2引数はポート番号
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
    parser.add_argument('--train_abst', type=str, default='train_abst.txt')
    parser.add_argument('--train_title', type=str, default='train_title.txt')
    parser.add_argument('--test_abst', type=str, default='test_abst.txt')
    parser.add_argument('--test_title', type=str, default='test_title.txt')
    parser.add_argument('--n_train', type=int, default=10000)
    args = parser.parse_args()

    titles, abstracts = read_db()

    idx = np.random.permutation(len(titles))

    f_abst = open(args.train_abst, 'w')
    f_title = open(args.train_title, 'w')
    for i in idx[:args.n_train]:
        f_abst.write(abstracts[i] + '\n')
        f_title.write(titles[i] + '\n')
    f_abst.close()
    f_title.close()

    f_abst = open(args.test_abst, 'w')
    f_title = open(args.test_title, 'w')
    for i in idx[args.n_train:]:
        f_abst.write(abstracts[i] + '\n')
        f_title.write(titles[i] + '\n')
    f_abst.close()
    f_title.close()

    
