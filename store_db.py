#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
python_arXiv_parsing_example.py

This sample script illustrates a basic arXiv api call
followed by parsing of the results using the 
feedparser python module.

Please see the documentation at 
http://export.arxiv.org/api_help/docs/user-manual.html
for more information, or email the arXiv api 
mailing list at arxiv-api@googlegroups.com.

urllib is included in the standard python library.
feedparser can be downloaded from http://feedparser.org/ .

Author: Julius B. Lucks

This is free software.  Feel free to do what you want
with it, but please play nice with the arXiv API!
"""

#import requests
import feedparser
import time
import argparse
from pymongo import MongoClient

# Base api query url
base_url = 'http://export.arxiv.org/api/query?';

# Search parameters
start = 0                     # retreive the first 5 results
total_results = 100000        # want 20 total results
results_per_iteration = 1000  # 5 results at a time
wait_time = 3                 # number of seconds to wait beetween calls




def extract_key(entry):
    return entry.id.split('/abs/')[-1]


def parse_entry(entry):
    entry_data = {'key'      : extract_key(entry),
                  'arxiv-id' : entry.id,
                  'Published': entry.published,
                  'Title'    : entry.title,
                  'Authors'  : ', '.join(author.name for author in entry.authors),
    }

    # get the links to the abs page and pdf for this e-print
    for link in entry.links:
        if link.rel == 'alternate':
            entry_data['abs page link'] = link.href
        elif link.title == 'pdf':
            entry_data['pdf link'] = link.href
                        
    # The journal reference, comments and primary_category sections live under 
    # the arxiv namespace
    try:
        journal_ref = entry.arxiv_journal_ref
    except AttributeError:
        journal_ref = 'No journal ref found'
    entry_data['Journal reference'] = journal_ref
    
    try:
        comment = entry.arxiv_comment
    except AttributeError:
        comment = 'No comment found'
    entry_data['Comments'] = comment
    
    entry_data['Primary Category'] = entry.tags[0]['term']
    
    # Lets get all the categories
    all_categories = [t['term'] for t in entry.tags]
    entry_data['All Categories'] = ', '.join(all_categories)
    
    # The abstract is in the <summary> element
    entry_data['Abstract'] = entry.summary

    return entry_data



parser = argparse.ArgumentParser(prog='store_db',
                                 usage='Get papers\'s metadata with arXiv API, and store it on DB',
                                 add_help=True, # -h/?help オプションの追加
)
parser.add_argument('-q', '--search_query', type=str, required=True,
                    help="ex: \"all:electron\"")
args = parser.parse_args()



#-----------------------------
# main
#-----------------------------
client = MongoClient('localhost', 27017) # 第2引数はポート番号
#collection = client.scraping.paper   # scraping データベースの paper コレクションを得る（ない場合は新規作成
#collection.drop()
collection = client.scraping.paper   # scraping データベースの paper コレクションを得る（ない場合は新規作成
collection.create_index('key', unique=True)

print('Searching arXiv for %s' % args.search_query)

# Opensearch metadata such as totalResults, startIndex, 
# and itemsPerPage live in the opensearch namespase.
# Some entry metadata lives in the arXiv namespace.
# This is a hack to expose both of these namespaces in
# feedparser v4.1
feedparser._FeedParserMixin.namespaces['http://a9.com/-/spec/opensearch/1.1/'] = 'opensearch'
feedparser._FeedParserMixin.namespaces['http://arxiv.org/schemas/atom'] = 'arxiv'

for i in range(start,total_results,results_per_iteration):
    
    # API call
    print('-' * 80)
    print("Results %i - %i" % (i,i+results_per_iteration))
    query = 'search_query=%s&start=%i&max_results=%i' % (args.search_query,
                                                         i,
                                                         results_per_iteration)
    feed = feedparser.parse(base_url+query)

    # 検索範囲を超えたら終了
    if int(feed.feed.opensearch_totalresults) < i:
        print("Search is completed.")
        break

    # print out feed information and opensearch metadata
    print('Feed title: %s' % feed.feed.title)
    print('Feed last updated: %s' % feed.feed.updated)
    print('totalResults for this query: %s' % feed.feed.opensearch_totalresults)
    print('itemsPerPage for this query: %s' % feed.feed.opensearch_itemsperpage)
    print('startIndex for this query: %s'   % feed.feed.opensearch_startindex)
    time.sleep(wait_time)

    # Run through each entry, and save on DB
    for entry in feed.entries:
        entry_data = parse_entry(entry)
        #print(entry_data)
        try:
            collection.insert_one(entry_data)
            #print("saving data on DB...")
        except:
            pass
            #print("This entry exists already.")

    time.sleep(wait_time)
