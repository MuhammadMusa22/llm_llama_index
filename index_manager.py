import pandas as pd
from llama_index.core import Document, VectorStoreIndex, ServiceContext, StorageContext, load_index_from_storage
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings


def load_data(file_name):
    """Load Excel data into a DataFrame."""
    df = pd.read_excel(file_name)
    return df


def create_documents(df):
    """Convert DataFrame rows into document objects."""
    documents = [
        Document(
            text=(
                f"The student name is {row['Name']}. "
                f"The father name is {row['Father Name']}. "
                f"The class number is {row['Class Number']}. "
                f"The fee paid is {row['Fee Paid']}."
            )
        )
        for _, row in df.iterrows()
    ]
    return documents


def create_index(documents, persist_dir="student_data_index"):
    """Create and save the index."""
    hf_embedding_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
    Settings.embed_model = hf_embedding_model
    Settings.llm = None
    # service_context = ServiceContext.from_defaults(embed_model=hf_embedding_model, llm=None)
    # index = VectorStoreIndex.from_documents(documents, service_context=service_context)

    index = VectorStoreIndex.from_documents(documents, embed_model=hf_embedding_model)
    index.storage_context.persist(persist_dir=persist_dir)
    print("Index created and saved successfully!")
    return index


def load_index(persist_dir="student_data_index"):
    # Configure the embedding model
    hf_embedding_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # Update settings globally
    Settings.embed_model = hf_embedding_model
    Settings.llm = None
    
    # Load the storage context and index
    storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
    index = load_index_from_storage(storage_context)
    
    return index

# def load_index(persist_dir="student_data_index"):
#     """Load the saved index."""
#     hf_embedding_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
#     service_context = ServiceContext.from_defaults(embed_model=hf_embedding_model, llm=None)
#     storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
#     index = load_index_from_storage(storage_context, service_context=service_context)
#     return index