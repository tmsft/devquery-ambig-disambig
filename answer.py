from prompts.answer_generation_prompt import answer_prompt

answer_generation_prompt_input = """
Query: #Query#,
valid_queries: #valid_queries#,
Language: #Language#,
Combined_WebResults: #Combined_WebResults#
Combined_Query_Topics: #Combined_Query_Topics#,
Combined_Query_Intents: #Combined_Query_Intents#
"""

def fill_answer_generation_data(prompt, query, valid_queries, language, combined_web_results, combined_query_topics, combined_query_intents):
    """
    Fill the answer generation prompt and input with the provided query and search results.
    """
    return (
        prompt
        .replace("#Query#", query)
        .replace("#valid_queries#", valid_queries)
        .replace("#Language#", language)
        .replace("#Combined_WebResults#", combined_web_results)
        .replace("#Combined_Query_Topics#", combined_query_topics)
        .replace("#Combined_Query_Intents#", combined_query_intents)
    )

def answer_generation(query, valid_queries, language, combined_web_results, combined_query_topics, combined_query_intents, client, deployment):
    """
    Generate an answer for a developer query based on search results.
    """
    filled_prompt = fill_answer_generation_data(answer_prompt, query, valid_queries, language, combined_web_results, combined_query_topics, combined_query_intents)
    filled_input = fill_answer_generation_data(answer_generation_prompt_input, query, valid_queries, language, combined_web_results, combined_query_topics, combined_query_intents)

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
    print("Answer Generation Response:", response.choices[0].message.content)
    return response.choices[0].message.content  