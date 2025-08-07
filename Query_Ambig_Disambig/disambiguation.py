from prompts.disambiguity_prompt import disambiguity_prompt

disambiguity_prompt_input = """
Query: #Query#,
explicit_intent:#explicit_intent#,
implicit_intent:#implicit_intent#,
interpretation_enumeration:#interpretation_enumeration#,
intent_clarity:#intent_clarity#,
reasoning_depth:#reasoning_depth#,
lexical_ambiguity:#lexical_ambiguity#,
contextual_ambiguity:#contextual_ambiguity#,
functional_ambiguity:#functional_ambiguity#,
key_interpretations:#key_interpretations#,
serp_interpretations:#serp_interpretations#,
difference_in_serp:#difference_in_serp#,
dominant_serp_interpretation:#dominant_serp_interpretation#,
serp_alignment_with_original_interpretation:#serp_alignment_with_original_interpretation#,
ambiguity_status:#ambiguity_status#,
ambiguity_level:#ambiguity_level#,
intent_coverage_required:#intent_coverage_required#,
decision_reasoning:#decision_reasoning#
"""

def fill_disambig_data(prompt, 
                       query, 
                       explicit_intent, 
                       implicit_intent, 
                       interpretation_enumeration, 
                       intent_clarity, 
                       reasoning_depth, 
                       lexical_ambiguity, 
                       contextual_ambiguity, 
                       functional_ambiguity, 
                       key_interpretations, 
                       serp_interpretations, 
                       difference_in_serp, 
                       dominant_serp_interpretation, 
                       serp_alignment_with_original_interpretation, 
                       ambiguity_status, 
                       ambiguity_level, 
                       intent_coverage_required, 
                       decision_reasoning):
    """
    Fill the disambiguation prompt and input with the provided query and ambiguity analysis.
    """
    return (
        prompt
        .replace("#Query#", query)
        .replace("#explicit_intent#", str(explicit_intent))
        .replace("#implicit_intent#", str(implicit_intent))
        .replace("#interpretation_enumeration#", interpretation_enumeration)
        .replace("#intent_clarity#", intent_clarity)
        .replace("#reasoning_depth#", reasoning_depth)
        .replace("#lexical_ambiguity#", lexical_ambiguity)
        .replace("#contextual_ambiguity#", contextual_ambiguity)
        .replace("#functional_ambiguity#", functional_ambiguity)
        .replace("#key_interpretations#", str(key_interpretations))
        .replace("#serp_interpretations#", str(serp_interpretations))
        .replace("#difference_in_serp#", difference_in_serp)
        .replace("#dominant_serp_interpretation#", str(dominant_serp_interpretation))
        .replace("#serp_alignment_with_original_interpretation#", serp_alignment_with_original_interpretation)
        .replace("#ambiguity_status#", ambiguity_status)
        .replace("#ambiguity_level#", ambiguity_level)
        .replace("#intent_coverage_required#", intent_coverage_required)
        .replace("#decision_reasoning#", decision_reasoning)
    )

def disambiguation(query, ambiguity_result, client, deployment):
    """
    Disambiguate a developer query based on the ambiguity analysis.
    """
    filled_prompt = fill_disambig_data(
        disambiguity_prompt, 
        query, 
        ambiguity_result["explicit_intent"], 
        ambiguity_result["implicit_intent"], 
        ambiguity_result["interpretation_enumeration"], 
        ambiguity_result["intent_clarity"], 
        ambiguity_result["reasoning_depth"], 
        ambiguity_result["lexical_ambiguity"], 
        ambiguity_result["contextual_ambiguity"], 
        ambiguity_result["functional_ambiguity"], 
        str(ambiguity_result["key_interpretations"]), 
        str(ambiguity_result["serp_interpretations"]), 
        ambiguity_result["difference_in_serp"], 
        ambiguity_result["dominant_serp_interpretation"], 
        ambiguity_result["serp_alignment_with_original_interpretation"], 
        ambiguity_result["ambiguity_status"], 
        ambiguity_result["ambiguity_level"], 
        ambiguity_result["intent_coverage_required"], 
        ambiguity_result["decision_reasoning"]
    )
    
    filled_input = fill_disambig_data(
        disambiguity_prompt_input,
        query,
        ambiguity_result["explicit_intent"], 
        ambiguity_result["implicit_intent"], 
        ambiguity_result["interpretation_enumeration"], 
        ambiguity_result["intent_clarity"], 
        ambiguity_result["reasoning_depth"], 
        ambiguity_result["lexical_ambiguity"], 
        ambiguity_result["contextual_ambiguity"], 
        ambiguity_result["functional_ambiguity"], 
        str(ambiguity_result["key_interpretations"]), 
        str(ambiguity_result["serp_interpretations"]), 
        ambiguity_result["difference_in_serp"], 
        ambiguity_result["dominant_serp_interpretation"], 
        ambiguity_result["serp_alignment_with_original_interpretation"], 
        ambiguity_result["ambiguity_status"], 
        ambiguity_result["ambiguity_level"], 
        ambiguity_result["intent_coverage_required"], 
        ambiguity_result["decision_reasoning"])

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
    print("Disambiguation Response:", response.choices[0].message.content)
    return(response.choices[0].message.content)
