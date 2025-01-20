# Toolformer Demonstration Notebook

## Overview  
[This Jupyter Notebook](https://github.com/limJhyeok/toolformer-experiment/blob/main/jupyter.ipynb) demonstrates the **Toolformer** approach, where a language model (GPT-J in this case) is augmented with API call capabilities to enhance its ability to complete tasks requiring external information. By inserting API calls during text generation and leveraging the responses, the model can dynamically incorporate real-time data into its outputs.

## Key Features  
- **API Call Integration**: Automatically inserts API calls into text where external information is required.  
- **Dynamic API Execution**: Executes API calls and incorporates their results into the output text.  
- **Loss-Based Evaluation**: Compares loss values for text with and without API call results to determine the optimal representation for fine-tuning.  
- **Model Fine-Tuning**: Uses the selected dataset for fine-tuning GPT-J to improve API-aware text generation.  
- **Iterative Inference**: Implements an iterative process where API results dynamically influence subsequent text generation.

## Usage  
### Prerequisites  
1. Install the required Python libraries:  
   ```bash
   pip install torch transformers
   ```
2. Ensure access to a compatible **GPU** for optimal performance.

### Notebook Workflow  
1. **Setup**:  
   - Load the GPT-J model and tokenizer from the Hugging Face Transformers library.  
   - Define a custom `Calendar` API tool for dynamic date-related queries.  

2. **Prompt and Data Preparation**:  
   - Define a prompt instructing the model to integrate API calls where necessary.  
   - Provide example input data for generating API calls.

3. **API Call Generation and Execution**:  
   - The model generates text with `[Calendar()]` API calls inserted where external information is needed.  
   - API calls are executed, and results are incorporated back into the text.

4. **Loss Calculation**:  
   - Compute loss for three variations of the text:
     - With API results (`[Calendar() -> Today is Thursday, November 30, 2023.]`)
     - With API placeholders (`[Calendar()]`)
     - Plain text (no API call)  
   - Compare losses to identify the most appropriate representation for fine-tuning.

5. **Fine-Tuning**:  
   - Create a fine-tuning dataset based on the loss comparison.  
   - Fine-tune the GPT-J model for better API-aware text generation.

6. **Inference**:  
   - Feed new inputs to the fine-tuned model.  
   - When the model generates an API call (e.g., `->`), execute the call, integrate the results, and continue decoding iteratively.

---

## Example  
### Input:  
```text
The store is never open on the weekend, so today it is closed.
```

### Output:  
```text
The store is never open on the [Calendar() -> Today is Saturday, November 25, 2023.] weekend, so today it is closed.
```

## Highlights  
- **Loss-Based Filtering**: The example shows how incorporating API results improves loss:  
  ```
  api + result loss: 2.84
  api without result loss: 2.98
  plain text loss: 3.83
  ```
- **Dynamic API Calls**: Enables the model to seamlessly interact with tools during text generation.  
- **Customizable APIs**: Easily extendable to include other APIs beyond `Calendar`.

---

## Learning Objectives  
1. Understand the integration of external API tools into language models.  
2. Explore loss-based filtering to evaluate the impact of API calls.  
3. Fine-tune language models for dynamic, tool-enhanced text generation.  
4. Implement iterative inference pipelines for real-time API utilization.

## References
1. [original paper(Toolformer: Language Models Can Teach Themselves to Use Tools)](https://arxiv.org/abs/2302.04761)
2. [lucidrains/Toolformer](https://github.com/lucidrains/toolformer-pytorch)

## Notes  
This notebook serves as an introduction to **Toolformer** principles. It can be extended with additional APIs and customized pipelines to address specific use cases, such as database queries, real-time weather updates, or knowledge retrieval systems.
