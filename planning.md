# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
## domain How production systems use Docker? I chose this domain because Docker is one of the most widely used technologies for deploying and managing applications in production environments. Understanding how real companies use Docker for containerization, scaling, monitoring, networking, and CI/CD pipelines is valuable for software engineering, DevOps, machine learning infrastructure, and distributed systems roles. Much of the practical knowledge comes from engineers sharing real-world experiences online rather than official Docker documentation. Official sources explain how Docker works, but discussions about production failures, security issues, deployment strategies, and operational best practices are often found in community forums and engineering blogs.
---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Docker Documentation|Official Doc | https://docs.docker.com|
| 2 | Docker Blog|Official Blog |https://www.docker.com/blog |
| 3 | Reddit Docker Community| Reddit| https://www.reddit.com/r/docker/?utm_source=chatgpt.com|
| 4 | Reddit DevOps Community|DevOps Forum | https://www.reddit.com/r/devops/?utm_source=chatgpt.com|
| 5 | Reddit Kubernetes Community|Reddit Kubernetes Forum |https://www.reddit.com/r/kubernetes/?utm_source=chatgpt.com |
| 6 | Stack Overflow|Docker Stack Overflow | https://stackoverflow.com/questions/tagged/docker?utm_source=chatgpt.com|
| 7 |Netflix Blog| Engineering Blog Netflix|https://netflixtechblog.com/?utm_source=chatgpt.com |
| 8 | Uber Engineering Blog |Uber Blog | https://www.uber.com/blog/engineering/?utm_source=chatgpt.com|
| 9 | Spotify Engineering Blog|Spotify Engineering |https://engineering.atspotify.com/?utm_source=chatgpt.com |
| 10 | Kubernetes official Doc|Kubernetes Official Doc |https://kubernetes.io/docs/?utm_source=chatgpt.com |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size: 500 tokens** 

**Overlap: 100 tokens**

**Reasoning:A 500-token chunk is large enough to preserve technical context such as deployment workflows, troubleshooting steps, or architectural explanations. The 100-token overlap helps prevent important information from being split across chunk boundaries.

If chunks are too small, retrieval may return isolated commands or configuration snippets without enough context to answer a question accurately. If chunks are too large, retrieval may return excessive irrelevant information, making it harder for the language model to identify the most relevant content.**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model: I will use the all-MiniLM-L6-v2 embedding model from Sentence Transformers because it provides a strong balance between retrieval quality, speed, and computational efficiency.**

**Top-k: 5 chunks**

**Production tradeoff reflection: Retrieving five chunks typically provides enough context while avoiding excessive noise. If too few chunks are retrieved, important information may be missed. If too many chunks are retrieved, irrelevant content can reduce answer quality and increase token usage.

Semantic search works because embeddings capture the meaning of text rather than relying solely on keyword matching. For example, a query about "container orchestration" may retrieve documents discussing "managing Docker containers with Kubernetes" even if the exact words do not match.**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | Why do companies use Docker in production environments?|Docker provides application portability, environment consistency, easier deployment, resource efficiency, and scalability across different infrastructure environments. |
| 2 |What are common security concerns when running Docker containers in production? | Running containers as root, vulnerable container images, exposed secrets, excessive container privileges, and outdated dependencies.|
| 3 |How does Docker support CI/CD pipelines? | Docker creates reproducible build environments, packages applications into containers, and allows consistent deployment across development, testing, and production environments.|
| 4 |Why do many production systems use Kubernetes alongside Docker? | Kubernetes automates container orchestration, scaling, service discovery, load balancing, and self-healing of containerized applications.|
| 5 | What is the difference between a Docker image and a Docker container?| A Docker image is a read-only template containing application code and dependencies, while a Docker container is a running instance of that image.|

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Noisy community discussions: Reddit and forum posts may contain conflicting advice, outdated practices, or opinions that are not universally accepted.

2. Rapidly changing technologies: Docker, Kubernetes, and container ecosystems evolve quickly, so older documents may become outdated.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->
# Architecture

```
+--------------------+
| Document Ingestion |
|--------------------|
| Sources:           |
| - Docker Docs      |
| - Reddit           |
| - Stack Overflow   |
| - Engineering Blogs|
+---------+----------+
          |
          v
+--------------------+
| Chunking           |
|--------------------|
| 500-token chunks   |
| 100-token overlap  |
+---------+----------+
          |
          v
+------------------------------+
| Embedding + Vector Store      |
|------------------------------|
| all-MiniLM-L6-v2             |
| Sentence Transformers        |
| ChromaDB                     |
+--------------+---------------+
               |
               v
+------------------------------+
| Retrieval                    |
|------------------------------|
| Cosine Similarity Search     |
| Top-k = 5 Chunks             |
+--------------+---------------+
               |
               v
+------------------------------+
| Generation                   |
|------------------------------|
| Groq LLM / Llama Model       |
| RAG Answer Generation        |
+------------------------------+
```




---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->
     <!--  I plan to use AI tools such as ChatGPT and GitHub Copilot for:

Generating and refining chunking strategies.
Assisting with document preprocessing and cleaning.
Creating embedding and retrieval pipeline code.
Generating evaluation questions and expected answers.
Debugging vector database and retrieval issues. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
