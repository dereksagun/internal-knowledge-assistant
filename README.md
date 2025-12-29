Internal Knowledge Assistant

An internal knowledge assistant that lets users ask questions about company documents and receive source-grounded answers using a Retrieval-Augmented Generation (RAG) pipeline. If the answer cannot be found in the documents, the system explicitly responds with “I don’t know.”

⸻

How It Works
	1.	A user submits a question
	2.	Relevant document chunks are retrieved using vector search
	3.	Results are aggregated and reranked to improve relevance
	4.	The model generates an answer only if supported by the retrieved context
	5.	Citations containing the document title and section are returned only when an answer is found

If no document clearly supports the question, the system responds with “I don’t know.”

⸻

Key Features
	•	Source-grounded answers
    Responses are generated only from retrieved documents, with explicit no-answer behavior to prevent hallucinations.
	•	Multi-stage retrieval
      Uses vector search, parent-document aggregation, and reranking to improve retrieval quality.
	•	Evaluation harness
      Includes a small test suite (30+ queries) to measure retrieval accuracy and citation correctness.
	•	Real-time backend
      Built with FastAPI and WebSockets to support interactive, multi-user sessions.
	•	Memory-efficient architecture
      Heavy dependencies are initialized once at startup and shared across sessions, reducing peak memory usage by ~23% and preventing per-session memory growth.
	•	Containerized deployment
      Dockerized for consistent local development and cloud deployment.

⸻

Tech Stack

Backend: Python, FastAPI, LangChain, ChromaDB, OpenAI API
Frontend: React, Tailwind CSS
Infra & Tools: Docker, Git

⸻

What I Learned
	•	How to design RAG systems that prioritize correctness over completeness
	•	How to evaluate retrieval quality instead of relying on anecdotal results
	•	How dependency lifecycle decisions affect memory usage and scalability
	•	How to build real-time backends that safely handle concurrent users
