from prompts.validation_prompt import validation_prompt

validation_prompt_input = """
Query: #Query#, 
ambiguity_status: #ambiguity_status#, 
ambiguity_level: #ambiguity_level#, 
decision_reasoning: #decision_reasoning#, 
reformulated_queries: #reformulated_queries#, 
dominant_tokens: #dominant_tokens#, 
disambiguation_reasoning: #disambiguation_reasoning#. 
"""

def fill_validation_data(prompt, query, ambiguity_status, ambiguity_level, decision_reasoning, reformulated_queries, dominant_tokens, disambiguation_reasoning):
    """
    Fill the validation prompt and input with the provided query and disambiguation results.
    """
    return (
        prompt
        .replace("#Query#", query)
        .replace("#ambiguity_status#", ambiguity_status)
        .replace("#ambiguity_level#", ambiguity_level)
        .replace("#decision_reasoning#", decision_reasoning)
        .replace("#reformulated_queries#", str(reformulated_queries))
        .replace("#dominant_tokens#", str(dominant_tokens))
        .replace("#disambiguation_reasoning#", disambiguation_reasoning)
    )

def validate_disambiguation(query, ambiguity_status, ambiguity_level, decision_reasoning, reformulated_queries, dominant_tokens, disambiguation_reasoning, client, deployment):
    """
    Validate the disambiguation results for a developer query.
    """
    filled_prompt = fill_validation_data(validation_prompt, query, ambiguity_status, ambiguity_level, decision_reasoning, reformulated_queries, dominant_tokens, disambiguation_reasoning)
    filled_input = fill_validation_data(validation_prompt_input, query, ambiguity_status, ambiguity_level, decision_reasoning, reformulated_queries, dominant_tokens, disambiguation_reasoning)

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
    print("Validation Response:", response.choices[0].message.content)
    return response.choices[0].message.content