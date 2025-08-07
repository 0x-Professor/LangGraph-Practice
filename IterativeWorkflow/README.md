# Iterative Workflows with LangGraph

This directory contains an example of implementing an iterative workflow using LangGraph. The example demonstrates how to create a feedback loop where the output of one iteration influences the next, allowing for continuous refinement of results.

## Example: AI-Powered Tweet Generator with Iterative Refinement

**File:** `practice.ipynb`

This example showcases an AI system that generates and iteratively refines tweets based on evaluation feedback. The workflow consists of three main components:

1. **Generator**: Creates tweets based on a given topic
2. **Evaluator**: Assesses the quality of the generated tweet
3. **Optimizer**: Refines the tweet based on evaluation feedback

The process repeats until either:
- The tweet meets quality standards, or
- A maximum number of iterations is reached

### Key Components

- **State Management**: Uses `TypedDict` to maintain the workflow state including:
  - Current tweet text
  - Evaluation results
  - Iteration count
  - Maximum allowed iterations

- **AI Models**:
  - Generator: Creative model for tweet generation
  - Evaluator: Critical model for quality assessment
  - Optimizer: Model for refining tweets based on feedback

- **Workflow Logic**:
  - Generate initial tweet
  - Evaluate against quality criteria
  - If approved, return the tweet
  - If needs improvement, refine and repeat
  - Stop after maximum iterations

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
4. Test with different topics and iteration limits
5. Observe how the tweet evolves through iterations

## Key Concepts

- **Iterative Refinement**: The system improves its output through multiple feedback loops
- **State Management**: Maintaining context across iterations
- **Model Specialization**: Different AI models for generation, evaluation, and optimization
- **Termination Conditions**: When to stop the iteration process

## Dependencies

- Python 3.8+
- langgraph
- langchain-google-genai
- pydantic

## Related Workflows

Check out other workflow examples in the parent directory for different LangGraph patterns and use cases.
