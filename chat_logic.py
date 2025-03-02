import llama_cpp as llama

path = r"C:\Users\miros\.cache\lm-studio\models\a\b\llama-3.2-3b-instruct-q8_0.gguf"

model = llama.Llama(model_path=path, n_ctx=10000, gpu_layers=-1)

def respond(history):
    response = model.create_chat_completion(
        messages=history,
        max_tokens=-1,
        temperature=0.8,
        top_k=40,
        repeat_penalty=1.1,
        top_p=0.95,
        min_p=0.05,
    )

    answer = response['choices'][0]['message']['content']
    history.append({'role': 'assistant', 'content': answer})

    return history
