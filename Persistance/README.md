# State Persistence with LangGraph

This directory demonstrates how to implement state persistence in LangGraph workflows, allowing you to save, load, and manage the state of your workflows across multiple executions. The example shows how to use checkpoints to maintain workflow state.

## Example: Joke Generation with State Persistence

**File:** `practice.ipynb`

This example implements a joke generation workflow with the ability to save and load its state. The workflow:
1. Generates a joke based on a given topic
2. Provides an explanation for the joke
3. Maintains conversation history
4. Supports state persistence across multiple runs

### Key Components

#### 1. State Management
- Uses `TypedDict` to define the workflow state:
  ```python
  class JokeState(TypedDict):
      topic: str
      joke: str
      explanation: str
  ```

#### 2. Checkpointing
- Implements `MemorySaver` for in-memory state persistence
- Enables saving and loading workflow states
- Maintains complete history of state changes

#### 3. Workflow Nodes
- **generate_joke**: Generates a joke based on the given topic
- **explain_joke**: Provides an explanation for the generated joke

## Setup

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. For the joke generation example, you'll need a Google API key for the Gemini model:
   - Obtain an API key from Google AI Studio
   - Set it in the notebook or as an environment variable

## Usage

### Running the Joke Generator
1. Open `practice.ipynb`
2. Set your Google API key if not using environment variables
3. Run the workflow with a topic:
   ```python
   config = {"configurable": {"thread_id": "1"}}
   result = workflow.invoke({"topic": "programming"}, config=config)
   ```

### State Management Features

#### Saving State
- The workflow automatically saves state after each step
- States are stored in memory using `MemorySaver`

#### Loading State
- Retrieve the full state history:
  ```python
  history = list(workflow.get_state_history(config=config))
  ```

#### Resuming Workflows
- The workflow can be resumed from any saved state
- Enables long-running processes and crash recovery

## Key Concepts

- **State Persistence**: Saving and loading workflow states
- **Checkpointing**: Creating restore points in workflow execution
- **Thread Management**: Handling multiple concurrent workflows
- **State History**: Tracking changes to workflow state over time

## Dependencies

- Python 3.8+
- langgraph
- langchain-google-genai (for joke generation)
- pydantic

## Related Workflows

Check out other workflow examples in the parent directory for different LangGraph patterns and use cases, including parallel processing and conditional logic.
