import csv
import random

from docarray import BaseDoc, DocList
from docarray.documents import ImageDoc, TextDoc


class Book(BaseDoc):
    title: str
    author: str
    price: float
    rating: float
    desc: TextDoc
    image: ImageDoc


book1 = Book(
    title="Hitchhiker's Guide to the Galaxy",
    author='Douglas Adams',
    price=15.99,
    rating=4.9,
    desc=TextDoc(
        text='"The Hitchhiker\'s Guide to the Galaxy" is a beloved science fiction novel that takes readers on a wild and hilarious journey through space. The story follows the misadventures of an unwitting human named Arthur Dent and his alien friend Ford Prefect as they travel through the galaxy, encountering bizarre characters and situations along the way. With its quirky humor and satirical take on the genre, "The Hitchhiker\'s Guide to the Galaxy" has become a classic of science fiction and a must-read for fans of the genre.'
    ),
    image=ImageDoc(
        url='https://m.media-amazon.com/images/I/51MzUz8rQcL._SX305_BO1,204,203,200_.jpg'
    ),
)

books = DocList[Book]()

with open('data/books.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    data = list(reader)

    for row in data:
        price = round(random.uniform(1.00, 30.00), 2)
        rating = round(random.uniform(0.00, 5.00), 2)

        book = Book(
            title=row['title'],
            author=row['author'],
            price=price,
            rating=rating,
            desc=TextDoc(text=row['desc']),
            image=ImageDoc(url=row['image']),
        )

        books.append(doc=book)

books.push('file://books.docarray')
