import textgrad as tg
import litellm

tg.set_backward_engine("litellm/gpt-4o", override=True)

# Step 1: Get an initial response from an LLM.
model = tg.BlackboxLLM("litellm/gpt-4o")

question_string = ("If it takes 1 hour to dry 25 shirts under the sun, "
                   "how long will it take to dry 30 shirts under the sun? "
                   "Reason step by step")

question = tg.Variable(question_string,
                       role_description="question to the LLM",
                       requires_grad=False)

answer = model(question)
print("~~~~ Question ~~~~")
print(question_string)
print("~~~~ Answer ~~~~")
print(answer)


######################################################################


 