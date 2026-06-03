import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_answer(question, contexts):
    """
    contexts: list of dicts -> {text, source}
    """

    context_text = "\n\n".join(
        [f"SOURCE: {c['source']}\nCONTENT: {c['text']}" for c in contexts]
    )

    system_prompt = """
You are a grounded QA system.

RULES:
- You MUST answer ONLY using the provided context.
- If the context does not contain the answer, say exactly:
  "I don't have enough information in the provided documents."
- Do NOT use outside knowledge.
- Every key claim MUST be supported by the context.
- Do NOT invent facts.
"""

    user_prompt = f"""
QUESTION:
{question}

CONTEXT:
{context_text}

OUTPUT FORMAT:
Answer:
<your answer>

Sources:
- list the source URLs used
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content