# Sequential Workflow with LangGraph

This directory demonstrates how to implement a sequential workflow using LangGraph. The example shows how to create a simple BMI (Body Mass Index) calculator that processes data through a series of steps.

## Example: BMI Calculation Workflow

**File:** `practice.ipynb`

This example implements a two-step BMI calculation workflow:
1. **Calculate BMI**: Computes the BMI using weight (kg) and height (m)
2. **Classify BMI**: Categorizes the BMI into standard weight categories

### Key Components

#### 1. State Management
- Uses `TypedDict` to define the workflow state:
  ```python
  class BMISTATE(TypedDict):
      weight_kg: float
      height_m: float
      bmi: float
      category: str
  ```

#### 2. Workflow Nodes
- **calculate_bmi**: Takes weight and height to compute BMI
- **classify_bmi**: Takes the calculated BMI and assigns a weight category:
  - Underweight: BMI < 18.5
  - Normal weight: 18.5 ≤ BMI < 25
  - Overweight: 25 ≤ BMI < 30
  - Obesity: BMI ≥ 30

#### 3. Graph Structure
- Linear workflow where the output of one node feeds into the next
- Simple and straightforward data flow
- Visual representation of the workflow is available in the notebook

## Setup

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Open `practice.ipynb`
2. Run the workflow with weight and height values:
   ```python
   result = workflow.invoke({
       'weight_kg': 70,  # Replace with desired weight in kg
       'height_m': 1.75  # Replace with desired height in meters
   })
   print(result)
   ```
3. View the calculated BMI and weight category in the output

## Key Concepts

- **Sequential Processing**: Data flows through nodes in a defined order
- **State Management**: Each node can read and modify the shared state
- **Type Safety**: Using `TypedDict` for clear state structure
- **Workflow Visualization**: Easy to understand the flow between nodes

## Dependencies

- Python 3.8+
- langgraph

## Related Workflows

Check out other workflow examples in the parent directory for different LangGraph patterns and use cases, including parallel processing and prompt chaining.
