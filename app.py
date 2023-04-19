import csv
import random

import numpy as np
from docarray import BaseDoc, DocList
from docarray.documents import ImageDoc, TextDoc
from docarray.index import HnswDocumentIndex

from helper import CSV_FILE, Book, clip_encode_desc

books = DocList[Book]()
db = HnswDocumentIndex[Book](work_dir='workspace')

with open(CSV_FILE, newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    data = list(reader)

    for row in data:
        price = round(random.uniform(1.00, 30.00), 2)
        rating = round(random.uniform(0.00, 5.00), 2)

        book = Book(
            title=row['title'],
            author=row['author'],
            price=price,
            rating=row['rating'],
            desc=row['desc'],
            # desc=TextDoc(text=row['desc']),
            image=ImageDoc(url=row['image']),
        )

        books.append(doc=book)

clip_encode_desc(books)

db.index(books)
