import os
import json
import streamlit as st
from openai import AzureOpenAI
from urllib.parse import urlparse
from webscraper import bing_search_headless
from ambiguity_detection import ambiguity_detection
from disambiguation import disambiguation
from validation import validate_disambiguation
from intent_classification import intent_classification
from answer import answer_generation


endpoint = os.environ.get("ENDPOINT_URL")
deployment = os.environ.get("DEPLOYMENT_NAME")
subscription_key = os.environ.get("AZURE_OPENAI_API_KEY")

client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2025-01-01-preview",
)

# --- Streamlit UI ---
st.markdown("""
    <style>
        .stApp {
            background: #F0EFF2;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }
    </style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="Query Ambiguity Detection and Disambiguation", layout="wide")
st.markdown("""
    <style>
        .custom-title {
            font-size: 50px;
            font-weight: 700;
            text-align: center;
            font-family: 'Segoe UI', sans-serif;
            color: #000000;
            padding: 0rem;
            margin-bottom: 20px;
            border-bottom: 2px solid #ccc;
            letter-spacing: -1.5px;
        }
    </style>
""", unsafe_allow_html=True)

# TITLE
st.markdown('<div class="custom-title">Query Ambiguity Detection and Disambiguation</div>', unsafe_allow_html=True)

# INPUT QUERY
st.markdown("""
    <style>
    /* Target the text input box itself */
    .stTextInput > div > div > input {
        background-color: #ffffff;
        color: #2c3e50;
        border: 2px solid #ccc;
        border-radius: 10px;
        padding: 0.7em 1em;
        font-size: 16px;
        font-family: 'Segoe UI', sans-serif;
        transition: all 0.3s ease;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }

    /* Style on focus */
    .stTextInput > div > div > input:focus {
        border-color: #4B4C7C;
        box-shadow: 0 0 5px rgba(75, 76, 124, 0.3);
        outline: none;
    }

    </style>
""", unsafe_allow_html=True)

query = st.text_input("Enter your developer query")

#RUN PIPELINE BUTTON
st.markdown("""
<style>

div.stButton > button:first-child {
    background-color: #2C2C2C;
    color: white;
    border: none;
    padding: 0.5em 1em;
    font-size: 15px;
    font-weight: bold;
    border-radius: 8px;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    transition: background-color 0.3s ease, transform 0.1s ease;
}
div.stButton > button:first-child:hover {
    background-color: #F0EFF2;
    transform: scale(1.02);
    color: black;
}
div.stButton > button:first-child:active {
    background-color: #2C2C2C;
    transform: scale(0.98);
}


/* Info button styling for all metric labels */
.info-btn {
    border: none;
    background: none;
    color: #007BFF;
    cursor: pointer;
    font-size: 14px;
    padding: 0;
    margin-left: 4px;
}
.info-btn:hover {
    color: #0056b3;
}
</style>
""", unsafe_allow_html=True)


# Actual button
if st.button("Run"):
    st.success("Pipeline triggered successfully!")
    with st.spinner("Scraping initial SERP results 🫧"):
        results = bing_search_headless(query)
        top_10_titles = results["Top_10_Titles"]
        top_10_snippets = results["Top_10_Snippets"]
        top_10_urls = results["Top_10_Urls"]
        print(top_10_titles)
        print("----------------------")
        print(top_10_snippets)
        titles = top_10_titles.split("#SEP#")
        snippets = top_10_snippets.split("#SEP#")
        urls = top_10_urls.split("#SEP#")
        st.subheader("📎Initial Web Scrape")
        with st.expander("View SERP Results", expanded=True): 
            for i, (title, snippet, url) in enumerate(zip(titles, snippets, urls), 1):
                # Extract domain for favicon
                domain = urlparse(url).netloc
                favicon_url = f"https://www.google.com/s2/favicons?sz=32&domain_url={domain}"
                # Create a row layout
                col1, col2 = st.columns([1, 12])
                with col1:
                    st.image(favicon_url, width=20)
                with col2:
                    st.markdown(f"**{i}. [{title}]({url})**  \n{snippet}")
        
        
    st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)
    
    with st.spinner("Detecting ambiguity 🫧"):
        ambiguity_result = json.loads(ambiguity_detection(query, top_10_titles, top_10_snippets, client, deployment))
        a = ambiguity_result
        if ambiguity_result["ambiguity_status"] == "Not Ambiguous":
            st.success("✅ The query is not ambiguous. No disambiguation is needed.")
        with st.container(border=True):
            st.subheader("📎Ambiguity Detection")
            with st.expander("**Metric Results**", expanded=True):
               
                with st.container(border=True):
                    st.markdown(
                        f"""
                        <div style="display: flex; justify-content: center;">
                            <table style="border-collapse: collapse; text-align: center;">
                                <tr>
                                    <th style="border: 1px solid #ddd; padding: 8px;">
                                        Ambiguity Status
                                        <button class='info-btn' title="Indicates whether the query is Ambiguous or Not Ambiguous.">ℹ️</button>
                                    </th>
                                    <th style="border: 1px solid #ddd; padding: 8px;">
                                        Ambiguity Level
                                        <button class='info-btn' title="Specifies the degree of ambiguity in the query from 'None', 'Low', 'Moderate', 'High'.">ℹ️</button>
                                    </th>
                                    <th style="border: 1px solid #ddd; padding: 8px;">
                                        Lexical Ambiguity
                                        <button class='info-btn' title="Measures ambiguity caused by word choice or phrasing from 'None', 'Low', 'Moderate', 'High'.">ℹ️</button>
                                    </th>
                                    <th style="border: 1px solid #ddd; padding: 8px;">
                                        Functional Ambiguity
                                        <button class='info-btn' title="Measures ambiguity caused by unclear purpose or function in the query from 'None', 'Low', 'Moderate', 'High'.">ℹ️</button>
                                    </th>
                                    <th style="border: 1px solid #ddd; padding: 8px;">
                                        Contextual Ambiguity
                                        <button class='info-btn' title="Measures ambiguity caused by missing or unclear context from 'None', 'Low', 'Moderate', 'High'.">ℹ️</button>
                                    </th>
                                </tr>
                                <tr>
                                    <td style="border: 1px solid #ddd; padding: 8px;">{a['ambiguity_status']}</td>
                                    <td style="border: 1px solid #ddd; padding: 8px;">{a['ambiguity_level']}</td>
                                    <td style="border: 1px solid #ddd; padding: 8px;">{a['lexical_ambiguity']}</td>
                                    <td style="border: 1px solid #ddd; padding: 8px;">{a['functional_ambiguity']}</td>
                                    <td style="border: 1px solid #ddd; padding: 8px;">{a['contextual_ambiguity']}</td>
                                </tr>
                            </table>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                   
                    col1, col2 = st.columns(2)
                    with col1:
                        with st.container(border=True):
                            st.markdown("""
                            <div style="display: flex; align-items: center;">
                                <strong>Explicit Intent</strong>
                                <button class='info-btn' title="Directly stated intent of the query — what the user explicitly asks for.">ℹ️</button>
                            </div>
                            """, unsafe_allow_html=True)
                            for i in a['explicit_intent']:
                                st.markdown(i)
                    with col2:
                        with st.container(border=True):
                            st.markdown("""
                            <div style="display: flex; align-items: center;">
                                <strong>Implicit Intent</strong>
                                <button class='info-btn' title="Underlying or implied intent inferred from the query or context.">ℹ️</button>
                            </div>
                            """, unsafe_allow_html=True)
                            for i in a['implicit_intent']:
                                st.markdown(i)

                    # # Row 4
                    # col1, col2, col3 = st.columns(3)
                    # with col1:
                    #     with st.container(border=True):
                    #         st.markdown("**Plausible Interpretations**")
                    #         st.markdown(f"{a['interpretation_enumeration']}")
                    # with col2:
                    #     with st.container(border=True):
                    #         st.markdown("**Intent Vagueness**")
                    #         st.markdown(f"{a['intent_clarity']}")
                    # with col3:
                    #     with st.container(border=True):
                    #         st.markdown("**Reasoning Depth Required**")
                    #         st.markdown(f"{a['reasoning_depth']}")

                    # Row 5: Two collapsible columns for key interpretations and SERP interpretations
                    col1, col2 = st.columns(2)
                    with col1:
                        with st.expander("**Key Interpretations**"):
                            for item in a["key_interpretations"]:
                                st.markdown(f"- {item}")
                    with col2:
                        with st.expander("**SERP Interpretations**"):
                            for item in a["serp_interpretations"]:
                                if "Dominant SERP Interpretation" in item:
                                    st.markdown(f"<span style='color:red; font-weight:bold;'>- {item}</span>", unsafe_allow_html=True)
                                else:
                                    st.markdown(f"- {item}")

                    # Row 6
                    col1, col2 = st.columns(2)
                    # with col1:
                    #     with st.container(border=True):
                    #         st.markdown("**Dominant SERP Interpretation**")
                    #         st.markdown(f"{a['dominant_serp_interpretation']}")
                    with col1:
                        with st.container(border=True):
                            st.markdown("""
                            <div style="display: flex; align-items: center;">
                                <strong>SERP Alignment</strong>
                                <button class='info-btn' title="Does the SERP reflect the interpretations found earlier?">ℹ️</button>
                            </div>
                            """, unsafe_allow_html=True)
                            st.markdown(f"{a['serp_alignment_with_original_interpretation']}")
                    with col2:
                        with st.container(border=True):
                            st.markdown("""
                            <div style="display: flex; align-items: center;">
                                <strong>Intent Coverage Required</strong>
                                <button class='info-btn' title="Can the intents be answered together or separately?">ℹ️</button>
                            </div>
                            """, unsafe_allow_html=True)
                            st.markdown(f"{a['intent_coverage_required']}")

                    # Row 7
                    with st.expander("**Decision Reasoning**"):
                        st.markdown(a["decision_reasoning"])


    if ambiguity_result["ambiguity_status"] == "Ambiguous":       
        st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)
        st.success("🔖 The query is ambiguous. Proceeding to disambiguation.")
        st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)

        with st.spinner("Disambiguating the query 🫧"):
            disambiguation_result = json.loads(disambiguation(query=query,
                                                              ambiguity_result=ambiguity_result,
                                                              client=client,
                                                              deployment=deployment))
        with st.container(border=True):
            st.subheader("📎Disambiguation Results")
            with st.expander("**Metric Results**", expanded=True):
                # Reformulated Queries (Collapsible)
                with st.expander("**Reformulated Queries**", expanded=True):
                    for k, v in disambiguation_result["reformulated_queries"].items():
                        st.markdown(f"**{k}.** {v}")
                col1, col2 = st.columns(2)
                with col1:
                    # Dominant Tokens (inline, comma-separated)
                    with st.container(border=True):
                        st.markdown("""
                            <div style="display: flex; align-items: center;">
                                <strong>Dominant Tokens</strong>
                                <button class='info-btn' title="List of core tokens or phrases that capture the unique meaning of all reformulated queries">ℹ️</button>
                            </div>
                            """, unsafe_allow_html=True)
                        tokens_inline = ", ".join(disambiguation_result["dominant_tokens"])
                        st.markdown(tokens_inline)
                with col2:
                    # Trigger Words (inline, comma-separated)
                    with st.container(border=True):
                        st.markdown("""
                            <div style="display: flex; align-items: center;">
                                <strong>Trigger Words</strong>
                                <button class='info-btn' title="List of short phrases from the original ambiguous query that most likely caused confusion">ℹ️</button>
                            </div>
                            """, unsafe_allow_html=True)
                            
                        triggers_inline = ", ".join(disambiguation_result["trigger_words"])
                        st.markdown(triggers_inline)

                # Reasoning (Collapsible)
                with st.expander("**Disambiguation Reasoning**"):
                    st.markdown(disambiguation_result["disambiguation_reasoning"])

        with st.spinner("Validating disambiguation 🫧"):
            validation_result = json.loads(validate_disambiguation(
                query=query,
                ambiguity_status=ambiguity_result["ambiguity_status"],
                ambiguity_level=ambiguity_result["ambiguity_level"],
                decision_reasoning=ambiguity_result["decision_reasoning"],
                reformulated_queries=disambiguation_result["reformulated_queries"],
                dominant_tokens=disambiguation_result["dominant_tokens"],
                disambiguation_reasoning=disambiguation_result["disambiguation_reasoning"],
                client=client,
                deployment=deployment
            ))
        
            st.subheader("📎Validation Results")
            with st.expander("**Metric Results**", expanded=True):
                with st.container(border=True):
                  
                    with st.expander("**Individual Query Validations**"):
                        for idx, query_info in enumerate(validation_result["individual_query_validations"]):
                            with st.expander(f"Reformulated Query {idx + 1}: {query_info['reformulated_query']}"):
                                for k, v in query_info.items():
                                    st.markdown(f"**{k.replace('_', ' ').capitalize()}**")
                                    st.write(v)
                  
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        with st.container(border=True):
                            st.markdown("""
                            <div style="display: flex; align-items: center;">
                                <strong>All Ambiguity Resolved</strong>
                                <button class='info-btn' title="Whether all the ambiguities present in the original query are effectively resolved by the disambiguated queries/">ℹ️</button>
                            </div>
                            """, unsafe_allow_html=True)
                            st.write(validation_result["all_ambiguities_resolved"])
                    with col2:
                        with st.container(border=True):
                            st.markdown("""
                            <div style="display: flex; align-items: center;">
                                <strong>All Disambiguation Conformed</strong>
                                <button class='info-btn' title="Whether all the disambiguated queries conform to the disambiguation reasoning/">ℹ️</button>
                            </div>
                            """, unsafe_allow_html=True)
                            st.write(validation_result["all_disambiguation_conformed"])
                    with col3:
                        with st.container(border=True):
                            st.markdown("""
                            <div style="display: flex; align-items: center;">
                                <strong>Dominant Tokens Relevant</strong>
                                <button class='info-btn' title="Whether the dominant tokens provided are relevant to the ambiguity reasoning provided">ℹ️</button>
                            </div>
                            """, unsafe_allow_html=True)
                            st.write(validation_result["dominant_tokens_relevant"])

                    with st.expander("**Valid Queries**", expanded=True):
                            for item in validation_result["valid_queries"].split("#SEP#"):
                                st.markdown(f"- {item}")

                    with st.container(border=True):
                        if validation_result["invalid_queries"]:
                            st.markdown("**Invalid Queries**")
                            st.write(", ".join([q["query"] for q in validation_result["invalid_queries"]]))
                        else:
                            st.markdown("**Invalid Queries**")
                            st.write("None")

                    with st.container(border=True):
                        st.markdown("**Validation Judgement**")
                        st.write(validation_result["validation_judgement"])

                    
                    with st.expander("**Validation Reasoning**"):
                        st.markdown(validation_result["validation_reasoning"])

                
        st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)
        if len(validation_result["invalid_queries"]) == 0:
            st.success("🔖 All the reformulated queries are valid. Proceeding to intent classification.")
        elif len(validation_result["valid_queries"]) == 0:
            st.error("❌ No valid queries found after validation. Please check the disambiguation process.")
        elif len(validation_result["valid_queries"]) > 0 and len(validation_result["invalid_queries"]) > 0:
            st.warning("🔖 Some queries were invalidated during validation. Proceeding with valid queries.")
        st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)
         
        st.subheader("📎SERP Scraping of Reformulated Valid Queries")
        with st.expander("**SERP Results for Reformulations**"):
            validated_queries = validation_result["valid_queries"]
            query_list = validated_queries.split("#SEP#")
            all_formatted_outputs = []
            combined_query_topics = ""
            combined_query_intents = ""
            q = 0
            for query in query_list:
                q += 1
                with st.spinner(f"Scraping and classifying intent for validated query {q} 🫧"):
                    results = bing_search_headless(query)
                    top_10_titles = results["Top_10_Titles"].split("#SEP#")
                    top_10_snippets = results["Top_10_Snippets"].split("#SEP#")
                    top_10_urls = results["Top_10_Urls"].split("#SEP#")

                    top_3_web_results = []
                    for i in range(min(3, len(top_10_titles))):
                        web_result = {
                            "title": top_10_titles[i],
                            "snippets": [top_10_snippets[i]],
                            "url": top_10_urls[i]
                        }
                        top_3_web_results.append(web_result)

                    combined_webresults = {
                        "web_search_results": top_3_web_results
                    }
                    all_formatted_outputs.append(combined_webresults)
                    
                    with st.expander(f"Top 3 Web Results for Reformulated Query {q}: `{query}`"):
                        for i, result in enumerate(top_3_web_results, 1):
                            domain = urlparse(result['url']).netloc
                            favicon_url = f"https://www.google.com/s2/favicons?sz=32&domain_url={domain}"
                            col1, col2 = st.columns([1, 12])
                            with col1:
                                st.image(favicon_url, width=20)
                            with col2:
                                st.markdown(f"**{i}. [{result['title']}]({result['url']})**  \n{result['snippets'][0]}")
                            st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)
                    
                    
                    
                    # Intent classification
                    intent_result = json.loads(intent_classification(query, client, deployment))
                    combined_query_topics += intent_result.get("query_topic", "") + ";"
                    combined_query_intents += intent_result.get("query_intent", "") + ";"

        st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)

        st.subheader("📎 Intent Classification Results")
        with st.expander("**Classification Results**", expanded=True):
            qi = combined_query_intents.split(";")
            qt = combined_query_topics.split(";")
            
          
            table_rows = ""
            for i in range(len(query_list)):
                table_rows += f"""
                <tr>
                    <td style="border:1px solid #ddd; padding:6px;">{query_list[i]}</td>
                    <td style="border:1px solid #ddd; padding:6px;">{qi[i]}</td>
                    <td style="border:1px solid #ddd; padding:6px;">{qt[i]}</td>
                </tr>
                """

         
            st.markdown(f"""
                <style>
                table {{
                    width: 100%;
                    border-collapse: collapse;
                }}
                th {{
                    background-color: #f4f4f4;
                    text-align: left;
                    padding: 8px;
                }}
                td {{
                    padding: 6px;
                }}
                </style>
                <table>
                    <tr>
                        <th>Query</th>
                        <th>Intent</th>
                        <th>Topic</th>
                    </tr>
                    {table_rows}
                </table>
            """, unsafe_allow_html=True)

        final_combined_string = "#SEP#".join([json.dumps(item, separators=(",", ":")) for item in all_formatted_outputs])
        print(final_combined_string)
        st.markdown("<hr style='margin:4px 0;'>", unsafe_allow_html=True)
    
        st.subheader("📎Final Answer Generation")
        with st.spinner("Generating final answer 🫧"):
            answer = answer_generation(
                query=query,
                valid_queries=validated_queries,
                language="en",
                combined_web_results=final_combined_string,
                combined_query_topics=combined_query_topics,
                combined_query_intents=combined_query_intents,
                client=client,
                deployment=deployment
            )
            with st.expander("**Answer**", expanded=True):
                st.markdown(answer, unsafe_allow_html=True)
