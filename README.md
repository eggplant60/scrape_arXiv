# scrape_arXiv

arXiv API を使って論文のメタデータを取得し、DB に突っ込みます。

## インストール

- [mongo DB](https://www.trifields.jp/how-to-install-mongodb-on-ubuntu-2751)

- pymongo

- feedparser

下の2つはpipでインストールします。


## HOW TO

1. API Calling and Storing metadata on DB  

    ```./store_db.py -q SEARCH_QUERY```

   例：カテゴリが機械学習であるエントリの検索：`./store_db.py -q cat:stat.ML`

   クエリの詳細は https://arxiv.org/help/api/user-manual#Appendices

2. Output metadata into a text

    ```./read_db.py --prefix PREFIX [--n_train N]```

    → 以下の6つのテキストファイルが生成される
    - [PREFIX]_train_abst.txt
    - [PREFIX]_train_title.txt
    - [PREFIX]_train_cat.txt
    - [PREFIX]_test_abst.txt
    - [PREFIX]_test_title.txt
    - [PREFIX]_test_cat.txt

    --n_train オプションで train のエントリ数を変更可能。残りが test になる。

## 注意

python 2.x では、read_db.py 実行時にエラー → python 3.x で実行してください。