# Conditional Workflows with LangGraph

This directory contains examples of implementing conditional workflows using LangGraph. These examples demonstrate how to create decision-based flows where the execution path changes based on certain conditions or inputs.

## Examples

### 1. Quadratic Equation Solver

**File:** `practice.ipynb`

This example implements a quadratic equation solver that demonstrates conditional branching based on the discriminant value:

- **State Management**: Uses `TypedDict` to define and manage the equation state
- **Conditional Flow**:
  - Calculates the discriminant of a quadratic equation
  - Branches to different handlers based on whether the roots are real or complex
  - Demonstrates state transitions in a computational workflow

### 2. Sentiment Analysis Workflow

**File:** `practice2.ipynb`

A more advanced example showing sentiment analysis with conditional responses:

- **Sentiment Detection**: Uses Google's Gemini model to analyze text sentiment
- **Structured Output**: Implements Pydantic models for type-safe output
- **Dynamic Response**: Generates different responses based on sentiment analysis
- **State Management**: Maintains conversation state across multiple steps

## Setup

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. For the sentiment analysis example, you'll need a Google API key:
   - Get an API key from Google AI Studio
   - Set it in the notebook or as an environment variable

## Usage

1. **Quadratic Equation Solver**:
   - Open `practice.ipynb`
   - Follow the cells to see how the workflow processes different equations
   - Observe how the flow changes based on the discriminant value

2. **Sentiment Analysis**:
   - Open `practice2.ipynb`
   - Update the API key if needed
   - Run the cells to see sentiment analysis in action
   - Experiment with different input texts to see conditional responses

## Key Concepts

- **State Management**: Using TypedDict and Pydantic models to maintain workflow state
- **Conditional Branching**: Directing flow based on computation results
- **Model Integration**: Connecting with external AI models for decision making
- **Workflow Definition**: Structuring complex, multi-step processes

## Dependencies

- Python 3.8+
- langgraph
- langchain-google-genai
- pydantic

## Related Workflows

Check out other workflow examples in the parent directory for more LangGraph patterns and use cases.
