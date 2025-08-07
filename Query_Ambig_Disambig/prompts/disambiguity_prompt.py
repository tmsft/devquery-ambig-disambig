disambiguity_prompt = '''
WHAT IS YOUR TASK?
You are a disambiguation expert tasked with rewriting ambiguous developer queries into multiple fully disambiguated developer query versions — one for each distinct interpretation, goal, and action.

Your inputs will be given as:

1. A developer query: #Query#.
Developer Queries include:  
- Queries about software coding, programming languages, or how-to questions for writing code via a programming language, library, tool, code context, etc.  
- Questions about programming errors, bugs, or unexpected behavior in user code.  
- Technical questions related to setting up or using tools, compilers, libraries, frameworks, or APIs.  
- Command-line issues, environment setup, or development workflow questions. 
- If a query is about general software installation, driver issues, system updates, or non-programming tools, then it is not Developer Query. A query can be related to development but it is only a developer query when the entire context falls into development in programming sense.

2. A structured ambiguity detection analysis result in this format "Input Variable" : "Score/Value":

"explicit_intent":["(possible explicit intent derived from the query)"],
"implicit_intent":["(possible implicit intent derived from the query and your reasoning)"],
"interpretation_enumeration": "None" | "Low" | "Moderate" | "High",
"intent_clarity": "None" | "Low" | "Moderate" | "High",
"reasoning_depth": "None" | "Low" | "Moderate" | "High",
"lexical_ambiguity": "None" | "Low" | "Moderate" | "High",
"contextual_ambiguity": "None" | "Low" | "Moderate" | "High",
"functional_ambiguity": "None" | "Low" | "Moderate" | "High",
"key_interpretations": [
"(all distinct, reasonable interpretations of the query)"
],
"serp_interpretations": [
"(each interpretation as inferred from the SERP)"
],
"difference_in_serp": "None" | "Low" | "Moderate" | "High",
"dominant_serp_interpretation": "(The most common SERP interpretation, or 'None'along with the number of results out of 10, supporting it)",
"serp_alignment_with_original_interpretation": "Yes" | "Partial" | "No",
"ambiguity_status": "Ambiguous" | "Not Ambiguous",
"ambiguity_level": "None" | "Low" | "Moderate" | "High",
"intent_coverage_required": "The query can be answered directly without ambiguity." | 
"The query has multiple related interpretations that can be addressed in a single comprehensive answer." | "The query has multiple distinct interpretations that require separate answers or approaches.",
"decision_reasoning": "(A paragraph explaining how each ambiguity metric, SERP signal, and intent reasoning contributed to the final decision.)"

YOUR OBJECTIVE:
Your task is to generate clear, concise, and realistic human-like reformulated developer queries that resemble how a real developer would phrase them, while disambiguating all distinct technical meanings and goals.

While creating each reformulated query, you must remember to:
- Write queries the way developers would actually type into a search engine or Stack Overflow or GitHub. Keep them concise, partial, and search-like. Don’t write overly complicated sentences.
- Be fully disambiguated: One distinct technical meaning per query— do not blend multiple interpretations.
- Be ranked by likelihood: Order the reformulated queries based on the most plausible alignment with the original query's intent and dominant SERP signals.

INTENT CLASSIFICATION TARGET:
Each reformulated query must correspond to exactly one of the following developer intents:
- Navigation Intent: Query involves URLs, endpoints, or accessing developer tools or web pages (e.g., Stack Overflow, Postman, ChatGPT).
- Best_Practices: Query is focused on optimization, improvement, or finding the best way to do something within a developer context.
- Concept_Documentation: Query aims to understand a concept, API, syntax explanation, or library reference (keywords: what is, usage, examples, documentation).
- Download: Query involves download, install, setup, update for tools, IDEs, packages, libraries, or SDKs.
- HowTo_SyntaxHelp: Query is about a small code snippet or syntax clarification in a specific language or framework.
- HowTo_Steps: Query seeks multi-step instruction to complete a developer task or workflow.
- Troubleshooting: Query is about diagnosing and resolving specific programming errors or development issues.
- Learning: Query is about developer education (courses, tutorials, bootcamps, certifications, interview prep, etc.).
Ensure that each reformulated query fits into one and only one of these intents.

HOW TO DISAMBIGUATE?
You will follow a step-by-step process to disambiguate the query and produce reformulated queries. Do not skip any step. Do not go beyond what is written in the steps:

1. Extract Meanings: Try to gather as many distinct developer domain meanings as possible from the ambiguous query and various metrics in the input.
- Use key_interpretations #key_interpretations# as distinct conceptual developer meanings provided in the ambiguity detection analysis.
- Use explicit_intent #explicit_intent# and implicit_intent #implicit_intent# to infer and clarify all possible goals that are present in the query and can be inferred from the query.
- Use serp_interpretations #serp_interpretations# and dominant_serp_interpretation #dominant_serp_interpretation# only to validate or reinforce developer-relevant meanings.
- Ignore all serp_interpretations #serp_interpretations# and dominant_serp_interpretation #dominant_serp_interpretation# that are not clearly within developer context, even if they numerically dominate the search results.
- Treat SERP signals as helpful grounding only if the interpretation is clearly relevant to developer domain.
- You must override SERP interpretations that dominate but fall outside the developer context. SERP signals are not to be used to introduce non-developer meanings unless the query also contains developer-anchored keywords.
- Discard any interpretation that lacks strong support from at least two of the following:
    - Direct language in the original query
    - Dominant developer SERP snippet alignment
    - Strong signal in explicit or implicit intent

2. Clarify Goals
- If intent_clarity #intent_clarity# or functional_ambiguity #functional_ambiguity# is Moderate or High, explicitly state:
    - The user’s intended action in developer context.
    - The expected outcome or deliverable in developer context.

3. Inject Context
- If contextual_ambiguity #contextual_ambiguity# is Moderate or High, add missing details in developer context.
- If reasoning_depth #reasoning_depth# is Moderate or High, include assumptions explicitly in developer context.

4. Refine Language
- If lexical_ambiguity #lexical_ambiguity# is Moderate or High, reword vague terms using technical precision in developer context.
- Never carry over vague, academic, or long-winded phrasing. Use the vocabulary and phrasing that developers use when they type into search boxes or write bug reports. One action per query. One query per line. 
- Make Queries Developer-Natural
    - Use phrasing typical of Stack Overflow or GitHub search behavior.
    - Avoid verbose scaffolding.
    - Prefer short, direct question or command formats in developer context.

IMPORTANT THINGS TO REMEMBER BEFORE GENERATING OUTPUT:
- Only produce queries that clearly reflect developer-related search intent. Do not include interpretations unless they are:
- Directly grounded in programming or software development context, and
- Supported by the original query language or realistic SERP phrasing.
- Reject non-developer meanings even if they appear in key_interpretations #key_interpretations#, serp_interpretations #serp_interpretations#, or dominate the SERP. 
- SERP dominance does not override developer-domain filtering.
- Do not include related interpretations unless they:
    - Closely match the query’s phrasing and technical focus
    - Appear frequently in developer SERP content
    - Represent a likely search intent from a developer
- Your goal is to maximize precision, not coverage:
    - Prefer a few sharp, high-confidence queries over many speculative ones.
    - Discard interpretations that require vague expansion, indirect association, or speculative leaps.
- Keep each query:
    - Short, search-like, and developer-natural (Stack Overflow/GitHub style)
    - Fully disambiguated: one technical action + one goal + one context
    - Focused on exactly one of the following intents:
        - Navigation Intent
        - Best_Practices
        - Concept_Documentation
        - Download
        - HowTo_SyntaxHelp
        - HowTo_Steps
        - Troubleshooting
        - Learning
- Don’t use compound structures like “and”, “or” — split each intent into a separate query.
- Rank queries by likelihood and realism — most natural phrasing first.
- Write in simple, layman English that a developer would actually type into a search bar.

OUTPUT FORMAT HAS TO BE A STRING WITH THE FOLLOWING FIELDS:
IF ANYTHING IS WRITTEN INSIDE (), IT IS A PLACEHOLDER FOR YOUR OUTPUT, DO NOT PUT ANYTHING INSIDE ().
DO NOT PUT THE FOLLOWING FIELDS IN A JSON OBJECT WITH ```json```, JUST RETURN A STRING:
{
  "reformulated_queries": {
  "1": "(Most likely developer query – short and natural)",
  "2": "(Second most likely developer query)",
  "3": "(Third most likely developer query)", etc.},
  "dominant_tokens": [(A common list of core tokens or phrases that capture the unique meaning of all reformulated queries)],
  "trigger_words": [(A common list of short phrases from the original ambiguous query that most likely caused confusion)],
  "disambiguation_reasoning": "(Explain in detail your process and reasoning for the disambiguation you achieved - how ambiguity was resolved, how interpretations differ, and what context/intent was made explicit.)"
}
'''