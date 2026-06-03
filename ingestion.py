import requests
import trafilatura
from tqdm import tqdm
import tiktoken
import re

# ----------------------------
# SOURCES (FIXED)
# ----------------------------
URLS = [
    "https://developer.hashicorp.com/terraform",
    "https://aws.amazon.com/blogs/containers/",
    "https://www.ibm.com/think/topics/docker",
    "https://aws.amazon.com/docker/",
    "https://www.geeksforgeeks.org/devops/introduction-to-docker/",
    "https://azure.microsoft.com/en-us/blog/topics/containers/",
    "https://kubernetes.io/blog/",
    "https://docker-curriculum.com/",
    "https://engineering.atspotify.com/",
    "https://kubernetes.io/docs/",
]

# ----------------------------
# CONFIG
# ----------------------------
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
MIN_CHARS = 250

encoding = tiktoken.get_encoding("cl100k_base")


# ----------------------------
# FETCH
# ----------------------------
def fetch(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
        }
        r = requests.get(url, headers=headers, timeout=15)

        if r.status_code != 200:
            print(f"[FETCH FAIL] {url} -> {r.status_code}")
            return None

        return r.text

    except Exception as e:
        print(f"[FETCH ERROR] {url}: {e}")
        return None


# ----------------------------
# CLEAN + EXTRACT
# ----------------------------
def clean(html, url):
    if not html:
        return ""

    text = trafilatura.extract(
        html,
        include_comments=False,
        include_tables=True,
        include_links=False,
        favor_recall=False
    )

    if not text or len(text) < MIN_CHARS:
        text = trafilatura.extract(
            html,
            include_comments=False,
            include_tables=True,
            include_links=False,
            favor_recall=True
        )

    if not text:
        return ""

    return post_clean(text)


# ----------------------------
# TEXT CLEANING
# ----------------------------
def post_clean(text):
    text = re.sub(r"\s+", " ", text)

    patterns = [
        r"cookie",
        r"subscribe",
        r"sign in",
        r"log in",
        r"accept all",
        r"privacy policy",
        r"terms of service"
    ]

    for p in patterns:
        text = re.sub(p, "", text, flags=re.IGNORECASE)

    return text.strip()


# ----------------------------
# TOKEN CHUNKING
# ----------------------------
def chunk_text(text, source):
    tokens = encoding.encode(text)

    chunks = []
    chunk_id = 0
    step = CHUNK_SIZE - CHUNK_OVERLAP

    for start in range(0, len(tokens), step):
        window = tokens[start:start + CHUNK_SIZE]

        if len(window) < 50:
            continue

        decoded = encoding.decode(window).strip()

        if len(decoded) < 80:
            continue

        chunks.append({
            "source": source,
            "chunk_id": chunk_id,
            "text": decoded
        })

        chunk_id += 1

    return chunks


# ----------------------------
# PIPELINE
# ----------------------------
def run():
    documents = []
    all_chunks = []

    seen_text = set()

    for url in tqdm(URLS, desc="Ingesting"):
        html = fetch(url)

        if not html:
            print(f"[SKIP] No response: {url}")
            continue

        text = clean(html, url)

        if not text or len(text) < MIN_CHARS:
            print(f"[WARN] Weak extraction: {url} ({len(text)} chars)")
            continue

        # light dedup (prevents repeated boilerplate across pages)
        if text in seen_text:
            continue
        seen_text.add(text)

        documents.append({
            "source": url,
            "text": text
        })

        chunks = chunk_text(text, url)

        if len(chunks) == 0:
            print(f"[WARN] No chunks generated: {url}")

        all_chunks.extend(chunks)

    return documents, all_chunks


# ----------------------------
# VALIDATION
# ----------------------------
def validate(docs, chunks):
    print("\n===== SAMPLE CLEAN DOCS =====")
    for d in docs[:3]:
        print("\nSOURCE:", d["source"])
        print(d["text"][:400])

    print("\n===== SAMPLE CHUNKS =====")
    for c in chunks[:5]:
        print("\nSOURCE:", c["source"])
        print("CHUNK:", c["chunk_id"])
        print(c["text"][:400])

    print("\n===== CHUNK COUNTS =====")
    counts = {}

    for c in chunks:
        counts[c["source"]] = counts.get(c["source"], 0) + 1

    for k, v in counts.items():
        print(k, "->", v, "chunks")

    print("\nTOTAL CHUNKS:", len(chunks))


# ----------------------------
# MAIN
# ----------------------------
if __name__ == "__main__":
    docs, chunks = run()
    validate(docs, chunks)