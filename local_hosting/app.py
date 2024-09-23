from flask import Flask, request, jsonify
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    '--model_hf_name_or_path',
    type=str,
    default='/dlabscratch1/public/llm_weights/llama3.1_hf/Meta-Llama-3.1-8B-Instruct',
    help='The name or path of the model to use (HF format)'
)

args = parser.parse_args()

app = Flask(__name__)

# Load the tokenizer and model
model_name = args.model_hf_name_or_path
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map='auto')
text_generator = pipeline('text-generation', model=model, tokenizer=tokenizer)

@app.route('/')
def index():
    return 'Hello from Flask!'

@app.route('/v1/completions', methods=['POST'])
def completion():
    data = request.get_json()
 
    # ~~~~~~~~~~~~~ Extract promp and parameters ~~~~~~~~~~~~~~~
    # Check if data is valid
    if not data or 'inputs' not in data:
        return jsonify({"error": "Invalid request format"}), 400

    prompt = data['inputs']
    #extract parameters, change this as you like
    parameters = data.get('parameters', {})
    parameters.pop("details")
    
    # ~~~~~~~~~~~~~ Generate text ~~~~~~~~~~~~~~~
    generated_texts = text_generator(prompt, num_return_sequences=1, **parameters)
    generated_text = generated_texts[0]['generated_text']
    
    # ~~~~~~~~~~~~~ Prepare response ~~~~~~~~~~~~~~~
    response = {
        "model": model_name,
        "choices": [{
            "message": {"content": generated_text},
            "index": 0,
            "logprobs": None,
            "finish_reason": "length"
        }],
        "generated_text": generated_text,
        "usage": {
            "prompt_tokens": len(tokenizer(prompt)['input_ids']),
            "completion_tokens": len(tokenizer(generated_text)['input_ids']),
            "total_tokens": len(tokenizer(prompt)['input_ids']) + len(tokenizer(generated_text)['input_ids'])
        }
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False) # Set debug=True for development