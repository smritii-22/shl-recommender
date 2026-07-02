import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client=genai.Client(
    api_key=os.getenv("Gemini_API_Key")
)

SYSTEM_PROMPT = """
You are an SHL Assessment Recommendation Assistant.

Rules:
1. Use ONLY the retrieved SHL assessments.
2. Never invent assessment names, URLs, durations, or test types.
3. Do NOT list URLs in the reply because URLs are already present in the recommendations array.
4. Do NOT repeat the full recommendation list in prose.
5. Write a concise, natural explanation in 60-120 words.
6. Mention why the assessments fit the user's role/skills.
7. If the retrieved assessments are weak matches, say that these are the closest catalogue matches.
8. Keep the tone professional and helpful.
9. If the user asks to compare assessments, provide a short comparison highlighting their purpose, strengths and suitable use cases before giving recommendations.
"""

def genreate_reply(conversation, recommendations):
    catalog="\n".join([
        f"""
Assessment: {r['name']}
Type: {r['test_type']}
Description: {r.get('description', '')}
Duration: {r.get('duration', '')}
Job Level: {", ".join(r.get("job_level", []))}
"""
        for r in recommendations
    ])

    prompt = f"""
{SYSTEM_PROMPT}

Conversation:
{conversation}

Retrieved Assessments:
{catalog}

Write only the conversational reply.
Do NOT output JSON.
Do NOT repeat the URLs.
Do NOT list every assessment again.
Simply explain why the retrieved assessments fit the user's request.
"""
    
    response=client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text



def rewrite_query(conversation):
    prompt=f"""
You are helping retrieve SHL assessments.
Given the conversation below, produce ONE complete search query that captures the user's latest intent.
If the user adds or removes constraints, include those changes clearly.
If the user says drop/remove/exclude something, include "exclude <item>" in the query.

Conversation:
{conversation}

Return ONLY the rewritten search query.
"""
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text.strip()



def decide_next_action(conversation):
    prompt = f"""
You are an SHL assessment assistant.

Decide if the agent has enough information to recommend assessments.

Return only one word:
ASK - if more clarification is needed
SEARCH - if enough information is available

Conversation:
{conversation}
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text.strip().upper()

    

def ask_clarification(conversation):
    prompt = f"""
You are an SHL assessment assistant.

Ask ONE short clarification question needed before recommending.
The question must be specific to the user's hiring need.

Conversation:
{conversation}
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text.strip()