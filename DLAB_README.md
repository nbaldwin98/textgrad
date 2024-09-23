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

3. Install the pytorch version that is compatible with your system. You can find the version of pytorch that is compatible with your system [here](https://pytorch.org/get-started/locally/). For runai, this one should work:
    ```shell
    pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
    ```

4. Set you API keys. Make sure to follow the instructions of [litellm](https://docs.litellm.ai/docs/providers) of how to name you environment variables. I'll give an example with [openai's API key](https://docs.litellm.ai/docs/providers/openai):
    ```shell
    conda env config vars set OPENAI_API_KEY="your-api-key"
    conda activate textgrad
    ```

5. Test it out !
    ```shell
    python litellm_basic_test.py 
    ```

# Model Naming

The name of the models follows the litellm naming (https://docs.litellm.ai/docs/providers/) but with a `litellm/`prefix in front. For example, the naming for litellm of gpt 4o mini is can be found (here) and is "gpt-4o-mini". So in textgrad, you would use `litellm/gpt-4o-mini`.

```
model = tg.BlackboxLLM("litellm/gpt-4o")
```

# Hosting your own models

For a detailed explanation of how to host your own models on runai, please refer [Neel's Tutorial](https://gist.github.com/Neel-Shah-29/57666e6c735a115d3eaf349071596bce).

IMPORTANT NOTE: I've added an example flask app in `local_hosting/app.py` that you can use to host your models locally (Neel's Flask app seems a bit outdated). 

I will nevertheless provide a brief overview of how to host your own models on runai:

1. Start a job. For example:
```shell
runai submit -i ghcr.io/jkminder/dlab-runai-images/pytorch:master --pvc dlab-scratch:/mnt --interactive -g 1.0 --job-name-prefix job -- sleep 43200
```
If all goes well, you should see something like this:
```shell
Job job-2dc80ac0d64c submitted successfully.
```

2. Attach to the job (change the job name to the one you got from the previous step):
```shell
runai bash job-2dc80ac0d64c
```

3. Activate your conda environment in the runai shell (IMPORTANT: you're conda environment has to be in dlabscratch1 or you won't be able to access it):
```shell
conda activate <PATH_TO_YOUR_CONDA_ENV>
```

4. cd into the directory where your model is stored and run the flask app. For me, it would be:
```shell
cd /dlabscratch1/baldwin/textgrad/
python local_hosting/app.py --model_hf_name_or_path <PATH_TO_YOUR_MODEL>
```
in my case:
```shell
python local_hosting/app.py --model_hf_name_or_path /dlabscratch1/public/llm_weights/llama3.1_hf/Meta-Llama-3.1-8B-Instruct
```

If all goes well you'll see something like this:
```shell
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://172.16.8.121:5000
Press CTRL+C to quit
 ```

You're app is now running on the server at the last address (in my case http://172.16.8.121:5000 )

COMMON ERRORS:
If you get an error like this:
```shell
ValueError: `rope_scaling` must be a dictionary with with two fields, `name` and `factor`, got {'factor': 8.0, 'low_freq_factor': 1.0, 'high_freq_factor': 4.0, 'original_max_position_embeddings': 8192, 'rope_type': 'llama3'}
```
Then upgrage the transformers library:
```shell
pip install transformers --upgrade
```

5. You're server should now be running. You can test it out by running with the following code:
```python
import textgrad as tg
from textgrad import get_engine

engine = get_engine("litellm/huggingface/Meta-Llama-3.1-8B-Instruct")
engine.base_url = "http://172.16.8.121:5000/v1/completions"

# Step 1: Get an initial response from an LLM.
model = tg.BlackboxLLM( engine=engine)

question_string = ("What is the average speed of a flying swallow")

question = tg.Variable(question_string,
                       role_description="question to the LLM",
                       requires_grad=False)

answer = model(question)
print("~~~~ Question ~~~~")
print(question_string)
print("~~~~ Answer ~~~~")
print(answer)
```

6. If you want to stop the server, you can do so by pressing `CTRL+C` in the runai shell and kill/delete the job.

