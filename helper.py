import os

import requests as rq
from docarray import BaseDoc, DocList
from docarray.documents import ImageDoc, TextDoc
from docarray.typing import NdArray
from dotenv import load_dotenv

load_dotenv()

CSV_FILE = 'data/books-20.csv'


class Book(BaseDoc):
    title: str
    embedding: NdArray[512] | None
    author: str
    price: float
    rating: float
    # desc: TextDoc
    desc: str
    image: ImageDoc


headers = {
    'Content-Type': 'application/json',
    'Authorization': os.getenv('JINA_TOKEN'),
}


def clip_encode_desc(docs):
    url = 'https://evolving-lacewing-2d90dee9c4-http.wolf.jina.ai/post'

    for i, doc in enumerate(docs, start=1):
        text_payload = {
            # 'data': [{'text': doc.desc.text}],
            'data': [{'text': doc.desc}],
            'execEndpoint': '/',
        }

        print(f'Encoding {i}/{len(docs)}')
        response = rq.post(url, json=text_payload, headers=headers)

        content = response.json()
        embedding = content['data'][0]['embedding']
        doc.embedding = embedding

    return docs
