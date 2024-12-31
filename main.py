import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from index_manager import load_data, create_documents, create_index, load_index
from query_handler import retrieve_context, use_hosted_llm

# Configuration
EXCEL_FILE = "test.xlsx"
PERSIST_DIR = "student_data_index"
HF_API_TOKEN = "input_hour_hugging_face_token"

# Initialize FastAPI app
app = FastAPI()

# Load or create index during startup
if not os.path.exists(PERSIST_DIR):
    print("Creating index...")
    df = load_data(EXCEL_FILE)
    documents = create_documents(df)
    create_index(documents, persist_dir=PERSIST_DIR)
else:
    print("Loading existing index...")

# Load the index
index = load_index(persist_dir=PERSIST_DIR)


# Define the JSON body schema
class QueryRequest(BaseModel):
    query: str  # Expecting a 'query' field in the JSON body

@app.post("/query")
async def query_index(request: QueryRequest):
    query = request.query
    print(request.query)
    
    try:
        # Retrieve context from the index
        context = retrieve_context(index, query)
        if not context:
            raise HTTPException(status_code=404, detail="No relevant context found for the query.")

        # Generate a response using hosted LLM
        hosted_response = use_hosted_llm(context, query, HF_API_TOKEN)
        return {"query": query, "answer": hosted_response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Run the FastAPI server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
