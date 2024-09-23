import textgrad as tg
from textgrad import get_engine

engine = get_engine("litellm/huggingface/Meta-Llama-3.1-8B-Instruct")
engine.base_url = !!!!TODO: PASTE THE URL LINK HERE!!! ##"http://172.16.3.2:5000/v1/completions"

# Step 1: Get an initial response from an LLM.
model = tg.BlackboxLLM( engine=engine)

question_string = (" Question 1: What is the average speed of a flying swallow")

question = tg.Variable(question_string,
                       role_description="question to the LLM",
                       requires_grad=False)

answer = model(question)
print("~~~~ Question ~~~~")
print(question_string)
print("~~~~ Answer ~~~~")
print(answer)