# app/main.py
import logging
from fastapi import FastAPI, HTTPException
from models import Document, LoadResponse, RetrieveRequest, RetrieveResponse
from utils import add_documents_to_index, retrieve_documents, documents
from pydantic import ValidationError

# Configure logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI"}

@app.post("/load", response_model=LoadResponse)
async def load_document(doc: Document):
    try:
        document_ids = add_documents_to_index([doc.content])
        return LoadResponse(document_id=document_ids[0], message="Document loaded successfully")
    except ValidationError as e:
        logging.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except AssertionError as e:
        logging.error(f"Assertion error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error: Dimension mismatch")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/retrieve", response_model=RetrieveResponse)
async def retrieve_document(request: RetrieveRequest):
    try:
        document_ids = retrieve_documents(request.query)
        contents = [documents[doc_id] for doc_id in document_ids if doc_id < len(documents)]
        return RetrieveResponse(document_ids=document_ids, contents=contents)
    except ValidationError as e:
        logging.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except IndexError as e:
        logging.error(f"Index error: {e}")
        raise HTTPException(status_code=404, detail="Document not found")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
