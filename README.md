# Llama Index QA Bot with Hugging Face

This repository demonstrates the basics of using **Llama Index** with Hugging Face models to build a simple Question-Answer (QA) chatbot. The bot processes and queries data from a students' fee structure stored in an Excel sheet. You can ask natural language questions like:  
- "Which students paid fees till June 2024?"  
- "List students who have pending transport fees."  

## Features
- **Hugging Face Model Integration**: Queries are processed using a Hugging Face model accessed over the Hugging Face API.  
- **Llama Index**: Used to connect and index the Excel sheet for efficient data querying.  
- **FastAPI Backend**: A FastAPI server handles requests from the frontend, communicates with the model, and returns responses.  
- **Excel Sheet Support**: Supports querying fee structure data from an Excel sheet.  

## Setup Instructions

### Prerequisites
- Python 3.8 or later
- A Hugging Face account with access to free models
- Installed dependencies listed in `requirements.txt`

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/llama-index-qa-bot.git
   cd llama-index-qa-bot
