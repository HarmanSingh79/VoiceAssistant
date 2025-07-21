from openai import OpenAI

client=OpenAI(api_key="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")

completion=client.chat.completions.create(
    model="gpt-4.1",
    messages=[
        {"role":"system","content":"You are a virtual assistant named Jarvis skilled in genral tasks like Alexa and Google Cloud.Give short "},
        {"role":"user","content":"what is coding?"}
    ]
)
print(completion.choices[0].message)

#paid api key so nt used on 20/07/2025,Sunday