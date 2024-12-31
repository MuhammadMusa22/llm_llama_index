import requests
import time
from transformers import pipeline


def retrieve_context(index, query, top_k=15):
    """Retrieve relevant context from the index."""
    response = index.as_query_engine(similarity_top_k=top_k).query(query)
    return str(response)


def use_hosted_llm(context, query, api_token, model_name="google/flan-t5-base", retries=3, delay=10):
    api_url = f"https://api-inference.huggingface.co/models/{model_name}"
    headers = {"Authorization": f"Bearer {api_token}"}
    # input_text = f"Context: {context}\nQuery: {query}\nAnswer:"
    input_text = (
    f"Context: {context}\n"
    f"Query: Based on the provided context, {query}\n"
    f"Answer with only the relevant details."
    )
    
    print(input_text)

    for attempt in range(retries):
        response = requests.post(api_url, headers=headers, json={"inputs": input_text})

        if response.status_code == 200:
            print('response is 200')
            print(response)
            return response.json()[0]["generated_text"]
        elif response.status_code == 503 and "loading" in response.text.lower():
            print(f"Model is still loading. Retrying in {delay} seconds... (Attempt {attempt + 1}/{retries})")
            time.sleep(delay)
        else:
            raise Exception(f"Error: {response.status_code}, {response.text}")
    
    raise Exception(f"Model did not load after {retries} attempts.")

