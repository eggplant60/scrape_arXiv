# scrape_arXiv

arXiv API を使って論文のメタデータを取得し、DB に突っ込みます。

## インストール

- [mongo DB](https://www.trifields.jp/how-to-install-mongodb-on-ubuntu-2751)

- pymongo

- feedparser

下の2つはpipでインストールします。


## HOW TO

1. API Calling and Storing metadata on DB  

    ```./store_db.py -q <search_query>```

   例：カテゴリが機械学習であるエントリの検索：`./store_db.py -q cat:stat.ML`

   クエリの詳細は https://arxiv.org/help/api/user-manual#Appendices

2. Output metadata into a text

    ```./read_db.py```

    → 以下の4つのテキストファイルが生成される
    - train_abst.txt
    - train_title.txt
    - test_abst.txt
    - test_title.txt

    --n_train オプションで train のエントリ数を変更可能。残りが test になる。
