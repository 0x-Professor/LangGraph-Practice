# Prompt Chaining with LangGraph

This directory demonstrates how to implement prompt chaining using LangGraph to create a multi-step content generation workflow. The example shows how to generate a blog post through a series of connected prompts.

## Example: Blog Generation Workflow

**File:** `practice.ipynb`

This example implements a two-step blog generation workflow:
1. **Create Outline**: Generates a detailed outline for a blog post based on a given topic
2. **Write Blog**: Uses the generated outline to create a complete blog post

### Key Components

#### 1. State Management
- Uses `TypedDict` to define the workflow state:
  ```python
  class BlogState(TypedDict):
      title: str
      outline: str
      content: str
  ```

#### 2. Workflow Nodes
- **create_outline**: Takes a blog topic and generates a structured outline
- **write_blog**: Takes the generated outline and expands it into a full blog post

#### 3. Graph Structure
- Linear workflow where the output of one node becomes the input of the next
- Visual representation of the workflow is available in the notebook

## Setup

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. For the blog generation example, you'll need a Google API key for the Gemini model:
   - Obtain an API key from Google AI Studio
   - Set it in the notebook or as an environment variable

## Usage

1. Open `practice.ipynb`
2. Set your Google API key if not using environment variables
3. Run the workflow with a topic:
   ```python
   initial_state = {"title": "Your Blog Topic Here"}
   final_state = workflow.invoke(initial_state)
   ```
4. View the generated outline and content in the `final_state` dictionary

## Key Concepts

- **Prompt Chaining**: Breaking down complex tasks into smaller, manageable prompts
- **State Management**: Passing data between different nodes in the workflow
- **Workflow Design**: Creating linear or branching sequences of operations
- **LLM Integration**: Using language models for content generation

## Dependencies

- Python 3.8+
- langgraph
- langchain-google-genai (for blog generation)

## Related Workflows

Check out other workflow examples in the parent directory for different LangGraph patterns and use cases, including parallel processing and state persistence.
