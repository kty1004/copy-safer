import openai

def change_parlance(user_text, api_key):
    openai.api_key=api_key
    sysyem_contents='너는 논문을 쓰는 한국 대학원생이야. 또한 너는 글의 양을 무조건 1.5배이상 늘릴 수 있어.'
    input_text=f'[{user_text}] 대괄호 안에 있는 글을 다듬어줘.'
    completion=openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {
                'role': 'user',
                'content': sysyem_contents+input_text
            },
            {'role':'system',
            'content':sysyem_contents}
        ],
        temperature=0
    )
    chat_res=completion.choices[0].message.content
    usage_token=completion.usage['total_tokens']

    print(chat_res, '\n', usage_token,': tokens are used.')
    return chat_res
