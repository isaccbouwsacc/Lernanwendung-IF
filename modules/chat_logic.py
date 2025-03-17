from openai import OpenAI

# Initialize LM Studio client
client = OpenAI(base_url="http://0.0.0.0:8000/v1", api_key="lm-studio")
MODEL = "gemma-3-12b-it"


def respond(history):
    response = client.chat.completions.create(
        model=MODEL,
        messages=history,
        max_tokens=-1,
        temperature=0.5,
        top_k=40,
        repeat_penalty=1.1,
        top_p=0.95,
        min_p=0.05
    )

    answer = response['choices'][0]['message']['content']
    history.append({'role': 'assistant', 'content': answer})

    return history
