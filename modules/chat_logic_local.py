from openai import OpenAI

# Initialize LM Studio client
client = OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="lm-studio")
MODEL = "gemma-3-12b-it"

def respond(history):
    response = client.chat.completions.create(
        model=MODEL,
        messages=history,
        max_tokens=-1,
        temperature=0.5
    )

    # Extract the content from the response
    answer = response.choices[0].message.content
    history.append({'role': 'assistant', 'content': answer})

    return history