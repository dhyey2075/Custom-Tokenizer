from fastapi import FastAPI
from pydantic import BaseModel
from tokenizer import Tokenizer
from typing import List

app = FastAPI()

tokenizer = Tokenizer()

@app.get("/")
def read_root():
    return {"Message": "Welcome to tokenizer API"}

@app.post("/get-tokens")
def get_tokens(text: str):
    try: 
        text.replace("%", " ")
        tokens = tokenizer.simple_tokens(text)
        return {"tokens": tokens}
    except Exception as e:
        return {"Error": str(e)}

@app.post("/get-encodings")
def get_encodings(tokens: List[str]):
    try:
        encodings = tokenizer.encode(tokens=tokens)
        return {"Encodings": encodings[0]}
    except Exception as e:
        return {"Error": str(e)}
    
@app.post("/get-token-to-id")
def get_encodings(tokens: List[str]):
    try:
        encodings = tokenizer.encode(tokens=tokens)
        return {"Token to id": encodings[1]}
    except Exception as e:
        return {"Error": str(e)}

@app.post("/get-decodings")
def get_decodings(encodings: List[int], token_to_id: dict):
    try:
        decodings = tokenizer.decode(encodings, token_to_id)
        return {"Decodings": decodings}
    except Exception as e:
        return {"Error": str(e)}
