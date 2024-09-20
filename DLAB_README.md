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

3. Set you API keys. Make sure to follow the instructions of [litellm](https://docs.litellm.ai/docs/providers) of how to name you environment variables. I'll give an example with [openai's API key](https://docs.litellm.ai/docs/providers/openai):
    ```shell
    conda env config vars set OPENAI_API_KEY="your-api-key"
    conda activate textgrad
    ```

4. Test it out !
    ```shell
    python litellm_basic_test.py 
    ```

# Model Naming

The name of the models follows the litellm naming (https://docs.litellm.ai/docs/providers/) but with a `litellm/`prefix in front. For example, the naming for litellm of gpt 4o mini is can be found (here) and is "gpt-4o-mini". So in textgrad, you would use `litellm/gpt-4o-mini`.

```
model = tg.BlackboxLLM("litellm/gpt-4o")
```