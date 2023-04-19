import os

import requests as rq
from docarray import BaseDoc, DocList
from docarray.documents import ImageDoc, TextDoc
from dotenv import load_dotenv

load_dotenv()


class Book(BaseDoc):
    title: str
    author: str
    price: float
    rating: float
    desc: TextDoc
    image: ImageDoc


print(os.getenv('JINA_TOKEN'))

headers = {
    'Content-Type': 'application/json',
    'Authorization': os.getenv('JINA_TOKEN'),
}


def clip_encode_desc(docs):
    url = 'https://evolving-lacewing-2d90dee9c4-http.wolf.jina.ai/post'

    for doc in docs:
        text_payload = {
            'data': [{'text': doc.desc.text}],
            'execEndpoint': '/',
        }

        response = rq.post(url, json=text_payload, headers=headers)

        content = response.json()
        embedding = content['data'][0]['embedding']
        doc.desc.embedding = embedding

    return docs
