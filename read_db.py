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
    categories = []
    
    for entry in collection.find():
        titles.append(re.sub('\s+', ' ', entry['Title']).replace('\n', ''))
        abstracts.append(re.sub('\s+', ' ', entry['Abstract']).replace('\n', ''))
        categories.append(re.sub('\s+', ' ', entry['Primary Category']).replace('\n', ''))
        #print('-' * 80)
        #time.sleep(1)
    print('number of the entries: {}'.format(collection.find().count()))
    return titles, abstracts, categories


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='read_db',
                                     usage='read DB and output train text',
                                     add_help=True, # -h/?help オプションの追加
    )
    parser.add_argument('--prefix', type=str, required=True)
    parser.add_argument('--n_train', type=int, default=69000)
    args = parser.parse_args()

    titles, abstracts, categories = read_db()

    n_entry = len(titles)
    
    if n_entry < args.n_train:
        print('n_train needs to be less than {}'.format(n_entry))
        exit()
        
    idx = np.random.permutation(n_entry)


    def save2txt(prefix, start, end):
        f_title = open(prefix + 'title.txt', 'w')
        f_abst = open(prefix + 'abst.txt', 'w')
        f_cat = open(prefix + 'cat.txt', 'w')

        for i in idx[start:end]:
            f_abst.write(abstracts[i] + '\n')
            f_title.write(titles[i] + '\n')
            f_cat.write(categories[i] + '\n')
        f_abst.close()
        f_title.close()
        f_cat.close()

    train_prefix = args.prefix + '_train_'
    save2txt(train_prefix, 0, args.n_train)

    test_prefix = args.prefix + '_test_'
    save2txt(test_prefix, args.n_train, n_entry)
    
