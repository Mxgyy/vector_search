from langchain.schema import Document
#from langchain.vectorstores import FAISS
from langchain_community.vectorstores import FAISS
import requests
import json

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
