from docarray import BaseDoc
from docarray.index import HnswDocumentIndex
from docarray.typing import NdArray


class MyDoc(BaseDoc):
    embedding: NdArray[128] | None = None
    text: str


db = HnswDocumentIndex[MyDoc](work_dir='./my_test_db')

import numpy as np
from docarray import DocList

# create some random data
docs = DocList[MyDoc](
    [
        MyDoc(embedding=np.random.rand(128), text=f'text {i}')
        for i in range(100)
    ]
)

# index the data
db.index(docs)

# create a query Document
query = MyDoc(embedding=np.random.rand(128), text='query')

# find similar Documents
matches, scores = db.find(query, search_field='embedding', limit=5)

print(f'{matches=}')
print(f'{matches.text=}')
print(f'{scores=}')
