import csv
import os

import requests as rq
from docarray import BaseDoc, DocList
from docarray.documents import ImageDoc, TextDoc
from docarray.typing import NdArray
from dotenv import load_dotenv

load_dotenv()

CSV_FILE = 'data/books-20.csv'


def load_csv(csv_file, max_docs=100, field_name='text'):
    docs = DocList[TextDoc]()

    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)

        for i, row in enumerate(data):
            if i == max_docs:
                break

            doc = TextDoc(text=row[field_name])

            docs.append(doc=doc)

    assert len(docs) == max_docs

    return docs


class Book(BaseDoc):
    title: str
    embedding: NdArray[512] | None
    author: str
    price: float
    rating: float
    # desc: TextDoc
    desc: str
    image: ImageDoc


class Toy(BaseDoc):
    product_name: str = ''
    embedding: NdArray[512] | None
    price: float = 0.0
    rating: float = 0.0
    desc: str = ''


headers = {
    'Content-Type': 'application/json',
    'Authorization': os.getenv('JINA_TOKEN'),
}


def clip_encode_desc(doc):
    url = 'https://evolving-lacewing-2d90dee9c4-http.wolf.jina.ai/post'

    text_payload = {
        # 'data': [{'text': doc.desc.text}],
        'data': [{'text': doc.text}],
        'execEndpoint': '/',
    }

    response = rq.post(url, json=text_payload, headers=headers)

    content = response.json()
    embedding = content['data'][0]['embedding']
    doc.embedding = embedding

    return doc
