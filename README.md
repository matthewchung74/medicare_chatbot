# Medicare Guide RAG Application

A conversational agent that answers questions about Medicare using information from the Medicare & You 2025 handbook.

## Live Demo

Try the live demo at: [Medicare Chatbot on Hugging Face](https://huggingface.co/spaces/matthewchung74/medicare_chatbot)

## Overview

This application uses Google's Agent Development Kit (ADK) to create a retrieval-augmented generation (RAG) system that can answer user queries about Medicare. The application provides a user-friendly Streamlit interface where users can ask questions and receive accurate, sourced information based on the official Medicare & You 2025 handbook.

## Features

- Conversational interface for asking Medicare-related questions
- Retrieval-augmented generation to provide accurate, sourced answers
- Proper handling of questions outside the agent's knowledge scope
- User session management for consistent conversation history

## Requirements

- Python 3.9+
- Google ADK API key
- OpenAI API key (optional, depending on configuration)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/medicare-rag-gcp.git
   cd medicare-rag-gcp
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with your API keys:
   ```
   GOOGLE_API_KEY=your_google_api_key
   GOOGLE_GENAI_USE_VERTEXAI=false
   OPENAI_API_KEY=your_openai_api_key  # if needed
   ```

   You can reference the `env.example` file for required environment variables.

## Usage

1. Start the Streamlit application:
   ```bash
   streamlit run app.py
   ```

2. Open your browser and navigate to the provided URL (typically http://localhost:8501)

3. Begin asking questions about Medicare in the chat interface

## How It Works

1. User queries are sent to the Medicare agent
2. The agent analyzes the query and retrieves relevant information from the Medicare handbook
3. Using AI capabilities from Google's Agent Development Kit, the agent generates a response based on the retrieved information
4. The response is presented to the user, including citations to specific sections of the Medicare handbook

## Project Structure

- `app.py`: Main Streamlit application
- `agent.py`: Agent configuration and logic
- `data/`: Directory containing Medicare handbook content
- `utils/`: Utility functions for agent operations

## Limitations

- The agent only has knowledge based on the Medicare & You 2025 handbook
- For questions outside its knowledge base, the agent will acknowledge limitations and may suggest contacting Medicare directly

## License

MIT License

Copyright (c) 2023

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.