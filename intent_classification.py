from prompts.intent_prompt import intent_prompt

intent_prompt_input = """
Query: #Query#
"""

def fill_intent_data(prompt, query):
    """
    Fill the intent classification prompt and input with the provided query.
    """
    return (
        prompt
        .replace("#Query#", query)
    )

def intent_classification(query, client, deployment):
    """
    Classify the intent of a developer query.
    """
    filled_prompt = fill_intent_data(intent_prompt, query)
    filled_input = fill_intent_data(intent_prompt_input, query)

    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": filled_prompt},
            {"role": "user", "content": filled_input}
        ],
        temperature=0,
        max_tokens=10000,
        top_p=1,
    )
    print("Intent Classification Response:", response.choices[0].message.content)
    return response.choices[0].message.content
