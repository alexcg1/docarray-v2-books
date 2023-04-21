import csv
import os

import requests as rq
from docarray import BaseDoc, DocList
from docarray.documents import TextDoc
from docarray.index import HnswDocumentIndex
from docarray.typing import NdArray
from docarray.utils.map import map_docs
from dotenv import load_dotenv

load_dotenv()

CSV_FILE = 'data/stackoverflow/Questions.csv'
FIELD_NAME = 'Title'
MAX_DOCS = 50
WORKDIR = 'workspace/simple/stackoverflow'
SEARCH_TERM = 'vectors'

headers = {
    'Content-Type': 'application/json',
    'Authorization': os.getenv('JINA_TOKEN'),
}


class MyTextDoc(TextDoc):
    embedding: NdArray[512] | None


def load_csv(csv_file, max_docs=100, field_name='text'):
    docs = DocList[MyTextDoc]()

    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)

        for i, row in enumerate(data):
            if i == max_docs:
                break

            if row[field_name] != '' or row[field_name] is not None:
                doc = MyTextDoc(text=row[field_name])
                docs.append(doc=doc)

    assert len(docs) == max_docs

    return docs


def clip_encode(doc):
    url = 'https://evolving-lacewing-2d90dee9c4-http.wolf.jina.ai/post'

    text_payload = {
        'data': [{'text': doc.text}],
        'execEndpoint': '/',
    }

    response = rq.post(url, json=text_payload, headers=headers)

    content = response.json()
    embedding = content['data'][0]['embedding']
    doc.embedding = embedding

    return doc


db = HnswDocumentIndex[MyTextDoc](work_dir=WORKDIR)

if db.num_docs() == 0:
    print(f'Index is empty. Will build index from {MAX_DOCS} records')

    docs = load_csv(CSV_FILE, MAX_DOCS, FIELD_NAME)

    print('Encoding records')
    encoded_docs = DocList[MyTextDoc](
        list(map_docs(docs, clip_encode, show_progress=True))
    )

    for doc in encoded_docs:
        assert hasattr(doc, 'embedding')

    # this doesn't seem to store vectors. only sqlite stuff in work_dir
    print('Storing records in Document Index')
    db.index(encoded_docs)

query = MyTextDoc(text=SEARCH_TERM)

print('Encoding query')
encoded_query = clip_encode(query)
assert hasattr(encoded_query, 'embedding')

# this breaks bc it can't find vectors
print('Matching query with records in index')
matches, scores = db.find(encoded_query, search_field='embedding', limit=5)

for (match, score) in zip(matches, scores):
    print(match.text)
    print(score)
    print('\n---\n')
