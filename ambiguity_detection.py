from prompts.ambiguity_prompt import ambiguity_prompt

ambiguity_prompt_input = """
Query: #Query#

Top 10 Titles:
#Top_10_Titles#

Top 10 Snippets:
#Top_10_Snippets#
"""

def fill_ambig_data(prompt, query, top_10_titles, top_10_snippets):
    """    
    Fill the ambiguity detection prompt and input with the provided query and search results.
    """ 
    return (
        prompt
        .replace("#Query#", query)
        .replace("#Top_10_Titles#", top_10_titles)
        .replace("#Top_10_Snippets#", top_10_snippets)
    )
    
def ambiguity_detection(query, top_10_titles, top_10_snippets, client, deployment):
    """
    Detect ambiguity in a developer query.       
    """
    filled_prompt = fill_ambig_data(ambiguity_prompt, query, top_10_titles, top_10_snippets)
    filled_input = fill_ambig_data(ambiguity_prompt_input, query, top_10_titles, top_10_snippets)   

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
    print("Ambiguity Detection Response:", response.choices[0].message.content)
    return(response.choices[0].message.content)