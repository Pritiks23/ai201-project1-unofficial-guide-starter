# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- This project focuses on how Docker is used in real production systems, including containerization workflows, orchestration with Kubernetes, CI/CD pipelines, scaling strategies, and security practices.

This domain is valuable because Docker is a foundational technology in modern software engineering and DevOps. However, practical knowledge—such as production failures, deployment strategies, and operational tradeoffs—is often not fully covered in official documentation. Instead, it is distributed across engineering blogs, cloud provider articles, and community-driven technical resources.

This makes it a strong candidate for a retrieval-augmented system because users need to synthesize information across multiple heterogeneous sources rather than rely on a single documentation site. -->

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | HashiCorp terraform|HashiCorp terraform | https://developer.hashicorp.com/terraform|
| 2 | Amazon Docker|Amazon Docker |https://aws.amazon.com/docker/ |
| 3 | AWS Container Blog| AWS Container Blog| https://aws.amazon.com/blogs/containers/|
| 4 | Geeks for Geeks|Geeks for Geeks | https://www.geeksforgeeks.org/devops/introduction-to-docker/|
| 5 | Microsoft Azure Containers Blog|Microsoft Azure Containers Blog |https://azure.microsoft.com/en-us/blog/topics/containers/ |
| 6 | Docker Curriculum|Docker Curriculum| https://docker-curriculum.com/|
| 7 |Kubernetes deep content| Kubernetes deep content|https://kubernetes.io/blog |
| 8 | IBM |IBM | https://www.ibm.com/think/topics/docker|
| 9 | Spotify Engineering Blog|Spotify Engineering |https://engineering.atspotify.com/?utm_source=chatgpt.com |
| 10 | Kubernetes official Doc|Kubernetes Official Doc |https://kubernetes.io/docs/?utm_source=chatgpt.com |


---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size: 500 tokens**

**Overlap: 100 tokens**

**Why these choices fit your documents: A 500-token chunk preserves enough semantic and technical context for infrastructure-related content such as Docker workflows, Kubernetes scaling behavior, and cloud architecture discussions. These topics often span multiple sentences describing systems rather than isolated facts.

A 100-token overlap prevents loss of meaning at chunk boundaries, especially for procedural or step-based explanations (e.g., deployment pipelines or configuration instructions), where a single step split across chunks would degrade retrieval quality. **

**Final chunk count: ~84 chunks (varied depending on page extraction quality and filtering)**

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used: all-MiniLM-L6-v2 from Sentence Transformers**

**Production tradeoff reflection: This model was chosen because it provides strong semantic representation while remaining lightweight and fast for local execution. It performs well for technical text where meaning is structured but not overly ambiguous.

In a production system, tradeoffs would include:

Larger embedding models (e.g., bge-large, OpenAI embeddings) improve semantic accuracy but increase cost and latency.
Multilingual models would be preferred if documentation spans multiple languages.
API-hosted embeddings improve quality and reduce local compute constraints but introduce cost and dependency on external services.
Context-aware embeddings (long-context models) may better handle large technical sections but reduce throughput.**

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction: “You are a grounded QA system.
Use ONLY the provided context.
If the answer is not contained in the context, respond: ‘I don’t have enough information.’
Do NOT use external knowledge.”**

**How source attribution is surfaced in the response: The retrieved chunks are formatted as:

[SOURCE: <url>]
<chunk text>

This ensures the model sees explicit provenance per chunk, reinforcing source-bound reasoning. Source attribution is not left to the model. Instead:

Retrieved chunks include explicit source metadata
The system returns a deduplicated list of source URLs alongside the generated answer
Each response includes a structured "sources" field returned programmatically from retrieval results**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Why do companies use Docker in production environments?| Portability, consistency, scalability, deployment efficiency|Correct explanation of Docker enabling consistent environments and fast deployment |Relevant | Accurate|
| 2 | What are security concerns in Docker?| Root containers, image vulnerabilities, exposed secrets, privileges|Mentioned container isolation limits and security risks | Relevant|Accurate |
| 3 |How does Docker support CI/CD? | Reproducible builds, consistent environments| Explained containerization for deployment pipelines| Relevant| Accurate|
| 4 |Why use Kubernetes with Docker? | Orchestration, scaling, self-healing|Correct explanation of orchestration layer |Relevant |Accurate |
| 5 |Docker image vs container?|Image = template, container = runtime instance |Clearly distinguished both concepts |Relevant | |Accurate|

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed: How does Kubernetes scaling work internally?**

**What the system returned: A general explanation of Kubernetes as an orchestration system, but no detailed scaling mechanics (HPA, cluster autoscaling, scheduling policies).**

**Root cause (tied to a specific pipeline stage): Retrieval limitation: the Kubernetes-related chunks were high-level documentation summaries rather than deep technical explanations. The embedding model retrieved general overview content instead of detailed scaling mechanics due to:

Chunk granularity being too coarse for specific subtopics
Source documents containing mostly introductory-level text in some sections**

**What you would change to fix it: ncrease chunk diversity by separating conceptual vs implementation sections
Improve retrieval with reranking or hybrid keyword + semantic search**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation: The spec enforced a clear pipeline structure (ingestion → chunking → embedding → retrieval → generation), which made it easier to debug each stage independently. This separation allowed retrieval issues to be identified without involving the LLM, which significantly reduced debugging complexity.**

**One way your implementation diverged from the spec, and why: Instead of using a vector database like ChromaDB, the implementation used in-memory embeddings with cosine similarity. This divergence was necessary due to dependency conflicts in the runtime environment (Python 3.14 compatibility issues with ChromaDB and related packages). The simplified approach ensured system stability while preserving retrieval correctness.**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI: My ingestion pipeline + chunking strategy + request to improve extraction robustness*
- *What it produced:A revised ingestion script with multi-pass Trafilatura extraction and better chunk filtering *
- *What I changed or overrode: I adjusted chunk size and removed unstable document sources that were failing extraction (e.g., Netflix/Uber pages)*

**Instance 2**

- *What I gave the AI:Error logs from ChromaDB + Gradio + Pydantic installation failures*
- *What it produced: Suggested fixes including dependency resolution and fallback retrieval design (cosine similarity without vector DB)*
- *What I changed or overrode: I removed ChromaDB entirely and replaced it with a lightweight embedding + numpy similarity implementation to ensure the system could run reliably in my environment*
