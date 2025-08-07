# Parallel Workflows with LangGraph

This directory contains examples of implementing parallel processing workflows using LangGraph. These examples demonstrate how to execute multiple independent tasks simultaneously and then combine their results.

## Examples

### 1. Cricket Statistics Analysis
**File:** `practice.ipynb`

This example demonstrates parallel processing of cricket statistics to calculate various performance metrics for a batsman. The workflow calculates three independent metrics in parallel:

- **Strike Rate**: (Runs / Balls) * 100
- **Balls per Boundary**: Total balls / (Fours + Sixes)
- **Boundary Percentage**: ((Fours*4) + (Sixes*6)) / Runs * 100

#### Key Components:
- **State Management**: Uses `TypedDict` to track:
  - Runs, balls, fours, sixes
  - Calculated metrics (strike rate, balls per boundary, boundary percentage)
  - Summary string combining all metrics

- **Parallel Processing**:
  - Three independent calculation nodes run in parallel
  - Results are combined in a summary node
  - Demonstrates fan-out/fan-in pattern

### 2. Essay Evaluation System
**File:** `practice2.ipynb`

This example shows a more complex parallel workflow for evaluating essays using multiple criteria simultaneously. The system evaluates an essay on different aspects in parallel:

- Language and Structure
- Content and Argumentation
- Originality and Insight
- Grammar and Style

#### Key Components:
- **Structured Output**: Uses Pydantic models for consistent evaluation criteria
- **Parallel Evaluation**: Multiple evaluators analyze different aspects simultaneously
- **Result Aggregation**: Combines individual evaluations into a comprehensive review
- **Google's Gemini Model**: Leverages AI for sophisticated essay analysis

## Setup

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. For the essay evaluation example, you'll need a Google API key for the Gemini model:
   - Obtain an API key from Google AI Studio
   - Set it in the notebook or as an environment variable

## Usage

### Cricket Statistics Example
1. Open `practice.ipynb`
2. Modify the initial state with cricket statistics:
   ```python
   initial_state = {
       "runs": 120,
       "balls": 100,
       "fours": 10,
       "sixes": 3
   }
   ```
3. Run the cells to see parallel processing in action

### Essay Evaluation Example
1. Open `practice2.ipynb`
2. Set your Google API key if not using environment variables
3. Modify the essay text as needed
4. Run the workflow to see parallel evaluation results

## Key Concepts

- **Parallel Execution**: Running multiple independent tasks simultaneously
- **State Management**: Maintaining and updating shared state across parallel nodes
- **Fan-out/Fan-in Pattern**: Splitting work into parallel tasks and combining results
- **Structured Output**: Using Pydantic models for consistent data validation
- **AI Integration**: Leveraging language models for content analysis

## Dependencies

- Python 3.8+
- langgraph
- langchain-google-genai (for essay evaluation)
- pydantic

## Related Workflows

Check out other workflow examples in the parent directory for different LangGraph patterns and use cases, including conditional logic and iterative refinement.
