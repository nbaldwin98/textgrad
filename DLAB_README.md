# Setup Instructions
1. Clone the repository
    ```shell
    git clone https://github.com/nbaldwin98/textgrad.git
    cd textgrad
    ```
2. Create a new conda environment and install the package
    ```shell
    conda create --n textgrad python=3.11
    conda activate textgrad
    pip install -e .
    ```

3. Set you API keys. Make sure to follow the instructions of [litellm]() of how to name you environment variables. I'll give an example with [openai's API key](https://docs.litellm.ai/docs/providers/openai):
    ```shell
    conda env config vars set OPENAI_API_KEY="your-api-key"
    conda activate textgrad
    ```
