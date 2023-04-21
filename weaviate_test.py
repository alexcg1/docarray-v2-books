from docarray import BaseDoc, DocList
from docarray.index.backends.weaviate import (EmbeddedOptions, =,
                                              embedded_options)

dbconfig = WeaviateDocumentIndex.DBConfig(embedded_options=embedded_options)

#  first start weaviate with docker-compose up


batch_config = {
    'batch_size': 20,
    'dynamic': False,
    'timeout_retries': 3,
    'num_workers': 1,
}

runtimeconfig = WeaviateDocumentIndex.RuntimeConfig(batch_config=batch_config)

dbconfig = WeaviateDocumentIndex.DBConfig(
    host='http://localhost:8080'
)  # Replace with your endpoint and/or auth settings


class TextDoc(BaseDoc):
    text: str = ''


store = WeaviateDocumentIndex[TextDoc](db_config=dbconfig)
store.configure(runtimeconfig)  # Batch settings being passed on


docs = DocList([TextDoc(text='foo')])
store.index(docs)
