from langchain.schema import Document
from langchain.vectorstores import FAISS
import requests
import json
import uuid


vdb_path = ".\\resources\\VDB.db"

class MyDocument:
    def __init__(self, page_content, metadata, id):
        self.page_content = page_content
        self.metadata = metadata
        self.id = id

def get_access_token():
        api_key = "RypA8KrTXHG1dag4xWHehqXX"
        secret_key = "tTETn96krReLMssRrdozE98VPiKfXKiv"
        url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={api_key}&client_secret={secret_key}"
        payload = json.dumps("")
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json().get("access_token")

chat_url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token=" + get_access_token()
embedding_url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/embeddings/bge_large_zh?access_token=" + get_access_token()

def embeddingOne(query):
        payload = json.dumps({
            "input": [query]
        })
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = requests.request("POST", embedding_url, headers=headers, data=payload)
        try:
            result = response.json().get("data")[0]['embedding']
        except Exception as e:
            print(response.json())
            #print(len(query))
            print(f"An error occurred: {e}")
        return result

def embeddingAll(paragraphs):
        embeddings = []
        i = 0
        for para in paragraphs:
            embeddings.append(embeddingOne(para))
            print(i)
            i += 1
        return embeddings



class Myembedding_funcxxx:
    def __init__(self):
        pass

    def embed_documents(self, paragraph):
        return embeddingAll(paragraph)
    
    def __call__(self, paragraph):
        return embeddingOne(paragraph)

files = ["hello,world", "goodbye,world", "hello,moon", "goodbye,moon"]
title = ['1.txt', '2.txt', '3.txt', '4.txt']
documents = []

for file, title in zip(files, title):
    doc = Document(page_content=file, metadata={"title": title})
    documents.append(doc)

vector_store = FAISS.from_documents(documents, Myembedding_funcxxx())
#vector_store = FAISS.load_local(vdb_path, Myembedding_funcxxx(),allow_dangerous_deserialization=True)
vector_store.add_documents([Document(page_content="the sun", metadata={"title": "5.txt"})])
#vector_store.save_local(vdb_path)
#vector_store.delete([5])

query = "the sun"
res = vector_store.search(query, k=10,search_type="similarity")

#vector_store.index()

print(len(res))

for doc in res:
    print(doc.metadata["title"], doc.page_content,doc.id)
    # vector_store.delete([doc.id])
    # vector_store.save_local(vdb_path)