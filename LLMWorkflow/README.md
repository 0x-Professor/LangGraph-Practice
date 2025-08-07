# LLM Workflow with LangGraph

This directory contains a basic example of implementing a Language Model (LLM) workflow using LangGraph. The example demonstrates how to create a simple question-answering system using Google's Gemini model.

## Example: Basic Q&A Workflow

**File:** `practice.ipynb`

This example showcases a straightforward implementation of a question-answering system using LangGraph and Google's Gemini model. It demonstrates the fundamental pattern of:

1. Defining a state structure for the workflow
2. Creating a node that processes the state using an LLM
3. Compiling and executing the workflow

### Key Components

- **State Management**: Uses `TypedDict` to define the workflow state:
  - `question`: The input question to be answered
  - `answer`: The generated response from the LLM

- **LLM Node**:
  - Takes a question from the state
  - Formats a prompt for the LLM
  - Invokes the Gemini model to generate a response
  - Updates the state with the answer

- **Workflow Definition**:
  - Creates a simple linear workflow with a single node
  - Connects the start node to the LLM node
  - Connects the LLM node to the end node

## Setup

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. You'll need a Google API key for the Gemini model:
   - Obtain an API key from Google AI Studio
   - Set it in the notebook or as an environment variable

## Usage

1. Open `practice.ipynb` in Jupyter Notebook
2. Set your Google API key if not using environment variables
3. Run the cells to define the workflow components
4. Test with different questions by modifying the `initial_state` dictionary
5. The workflow will return the state containing both the question and the generated answer

## Key Concepts

- **State Management**: Using TypedDict to maintain workflow state
- **LLM Integration**: Connecting to Google's Gemini model for text generation
- **Workflow Definition**: Creating and compiling a simple workflow
- **Prompt Engineering**: Basic example of formatting prompts for the LLM

## Dependencies

- Python 3.8+
- langgraph
- langchain-google-genai

## Extending the Example

This basic example can be extended to:
- Add more sophisticated prompt engineering
- Include multiple LLM nodes in sequence
- Implement conditional logic based on LLM responses
- Add error handling and retry mechanisms

## Related Workflows

Check out other workflow examples in the parent directory for more complex LangGraph patterns and use cases, including conditional logic and iterative refinement.
