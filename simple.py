from docarray import DocList
from docarray.documents import TextDoc
from docarray.index import HnswDocumentIndex
from docarray.utils.map import map_docs

from helper import clip_encode_desc, load_csv

CSV_FILE = 'data/toys/toys.csv'
MAX_DOCS = 20
WORKDIR = 'workspace/simple'

db = HnswDocumentIndex[TextDoc](work_dir=WORKDIR)

if db.num_docs() == 0:
    print(f'Index is empty. Will build index from {MAX_DOCS} records')

    docs = load_csv(CSV_FILE, MAX_DOCS, 'product_description')
    print('Encoding records')
    encoded_docs = DocList[TextDoc](
        list(map_docs(docs, clip_encode_desc, show_progress=True))
    )

    print('Storing records in Document Index')
    db.index(encoded_docs)

query = TextDoc(
    text='Model trainset with real transforming action',
)

print('Encoding query')
encoded_query = clip_encode_desc(query)

print('Matching query with records in index')
matches, scores = db.find(
    encoded_query, search_field='embedding', limit=5
)   # this breaks

for match in matches:
    print(match.desc, '\n---\n')
