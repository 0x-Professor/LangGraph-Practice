# LangGraph Practice Examples

This repository contains practical examples of different workflow patterns implemented using LangGraph. Each example demonstrates a specific type of workflow that can be used for various data processing and automation tasks.

## Table of Contents

- [Overview](#overview)
- [Workflow Examples](#workflow-examples)
- [Installation](#installation)
- [Common Dependencies](#common-dependencies)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Overview

LangGraph is a powerful library for creating and managing workflows in Python. This repository provides practical examples of different workflow patterns that can be used as a reference or starting point for your own projects.

## Workflow Examples

| Workflow Type | Description | Example |
|--------------|-------------|---------|
| [Sequential](sequentialWorkflow) | Linear processing of data through a series of steps | BMI Calculator |
| [Conditional](ConditionalWorkflow) | Branching logic based on conditions | Quadratic Equation Solver, Sentiment Analysis |
| [Iterative](IterativeWorkflow) | Repeated processing with refinement | AI-Powered Tweet Generator |
| [Parallel](ParallelWorkflow) | Simultaneous execution of independent tasks | Cricket Statistics, Essay Evaluation |
| [State Persistence](Persistance) | Maintaining state across workflow executions | Joke Generator with Memory |
| [Prompt Chaining](PromptChaining) | Chaining multiple LLM prompts together | Blog Post Generator |
| [LLM Integration](LLMWorkflow) | Basic LLM interaction | Simple Q&A System |
| [ChatBot](ChatBot) | Interactive chat interface | Full-stack AI ChatBot |

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/0x-Professor/LangGraph-Practice.git
   cd LangGraph-Practice
   ```

2. Navigate to the specific workflow directory you're interested in:
   ```bash
   cd workflow_directory_name
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Common Dependencies

Most examples require:
- Python 3.8+
- langgraph
- Jupyter Notebook (for .ipynb examples)

Additional dependencies for specific examples:
- langchain-google-genai (for LLM integration examples)
- pydantic (for data validation)
- fastapi, streamlit (for web interfaces)

## Usage

1. Navigate to the specific workflow directory
2. Follow the instructions in the workflow's README.md
3. Run the example:
   - For Jupyter notebooks: `jupyter notebook practice.ipynb`
   - For Python scripts: `python main.py`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.