#!/usr/bin/env python
from re import I
from bs4 import BeautifulSoup as bs
import ebooklib
from ebooklib import epub
import os 
import argparse


def is_contains_chinese(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False

def get_catalog(book_path):
  book = epub.read_epub(book_path)
  catalog = [doc.get_content()
              for doc in book.get_items_of_type(ebooklib.ITEM_NAVIGATION)][0]

  soup = bs(catalog,features="xml")
  catalogs = [text_tag.get_text() for text_tag in soup.find_all('text')]
  print("### {}".format(catalogs[0]))
  for cata in catalogs[1:]: 
    if is_contains_chinese(cata):
      pass
    else:
      print(cata)

  print("\n----\n")




if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        "import epub book and export xlsx file which contains the word list of book"
    )
    parser.add_argument("--rootDir", help="the root dir of epub books", type=str)
    args = parser.parse_args()

    for (root, dirs, files) in os.walk(args.rootDir, topdown=True):
      for file in files:
        path = os.path.join(root, file)
        filename, file_extension = os.path.splitext(path)
        if file_extension != ".epub":
            continue
        get_catalog(path)