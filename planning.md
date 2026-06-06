# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

My project domain is SFSU Computer Science student experiences. The guide will answer questions about CS professors, course difficulty, elective requirements, easy classes, and general opinions about the SFSU CS program.

This knowledge is valuable because official university pages usually only show formal course descriptions, degree requirements, and catalog information. They do not show honest student experiences about workload, teaching style, grading, course organization, or whether a class is considered easy or difficult.
---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| #     | Source                |    Description             |       URL or location          |
|-------|-----------------------|----------------------------|-----------------|
     1    Rate My Professors | Anthony Souza professor reviews | data/raw/anthony_souza_rmp.docx
     2	Rate My Professors | Duc Ta professor reviews    |  data/raw/duc_ta_rmp.docx
     3	Rate My Professors | Jose Ortiz-Costa professor reviews | 	data/raw/jose_ortiz_costa_rmp.docx
     4	Rate My Professors | Matt Pico professor reviews |  data/raw/Matt_pico_rmp.docx
     5	Rate My Professors | Robert Bierman professor reviews |  data/raw/robert_bierman_rmp.docx
     6	Reddit r/SFSU | Student discussion about best CS professors	|  data/raw/reddit_best_cs_professors.docx
     7	Reddit r/SFSU | Student discussion about CS elective requirements |	data/raw/reddit_cs_elective_requirements.docx
     8	Reddit r/SFSU | Student discussion about the SFSU CS program |	data/raw/reddit_cs_program_sfsu.docx
     9	Reddit r/SFSU | Student discussion about CSC 415 professor recommendations |	data/raw/           reddit_csc415_professor_recommendations.docx
     10	Reddit r/SFSU | Student discussion about easy classes at SFSU | 	data/raw/reddit_easy_classes_sfsu.docx


---
Chunking Strategy

Chunk size: 350 characters

Overlap: 75 characters

Reasoning:

My dataset mostly contains short student reviews, Reddit comments, and summarized discussion posts. These documents are not long academic articles, so very large chunks would likely mix unrelated reviews together. A 350-character chunk should usually capture one complete student opinion or one small group of related sentences.

The 75-character overlap helps preserve context when an important statement falls near the boundary between two chunks. For example, a comment might mention a professor in one sentence and then describe the workload in the next sentence. Overlap makes it more likely that both pieces of information stay available during retrieval.

If chunks are too small, the system may retrieve incomplete opinions without enough context. If chunks are too large, the system may retrieve irrelevant details about other professors, courses, or comments.

Retrieval Approach

Embedding model: all-MiniLM-L6-v2 using sentence-transformers

Top-k: 4 chunks per query

Production tradeoff reflection:

I chose all-MiniLM-L6-v2 because it is free, lightweight, runs locally, and is recommended for this project. It should work well for a small dataset of student reviews and Reddit comments.

I will use ChromaDB as the vector database. For each question, the system will retrieve the top 4 most relevant chunks. Top-k = 4 should provide enough context for the answer while avoiding too many unrelated chunks.

Semantic search is useful because users may phrase questions differently from the documents. For example, a user might ask, “Is CSC 415 hard?” while the document says, “CSC 415 is one of the hardest CS classes.” Semantic embeddings can connect those meanings even without exact word matching.

If this system were used in production, I would compare embedding models based on accuracy, cost, speed, context length, and support for informal student language. I would also consider whether the model supports multiple languages and whether it can handle larger document collections efficiently.

Evaluation Plan
#	Question	Expected answer
1	What do students say about Robert Bierman and CSC 415?	
Students say CSC 415 is difficult regardless of professor, but Bierman’s course is organized and he is knowledgeable. Some students may find his teaching style strict or direct.
2	Are CS students required to complete 12 units of electives?	
Yes. The Reddit discussion says CS majors need to complete 12 units of CS electives for graduation.
3	What do students say about the SFSU CS program overall?	
Students say the program can be useful, but success depends heavily on personal effort, projects, interview preparation, internships, and skills outside of coursework.
4	What easy classes do students recommend at SFSU?	
Students recommend classes such as LABR 250, BIO 318, California Food, Wine and Culture, and some film courses as easier or lower-workload options.
5	Which sources discuss recommended CS professors?	
The system should retrieve professor review documents and the Reddit best CS professors document, especially sources about Anthony Souza, Duc Ta, Jose Ortiz-Costa, Matt Pico, Robert Bierman, and student professor recommendations.

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Student reviews are subjective and sometimes conflicting. One student may describe a professor as helpful while another may describe the same professor as difficult or strict.
2. Reddit documents can contain noisy text such as ads, usernames, votes, deleted comments, or unrelated replies. The ingestion process needs to focus on useful student-generated content.
3. Retrieval may return the wrong professor or course if two documents use similar language about difficulty, workload, or grading.
4. Source attribution may be challenging if chunks lose metadata about which document they came from. I need to preserve filename/source information for each chunk.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->
                    Source Documents
                    (10 .docx files from Rate My Professors + Reddit)
                         |
                         |
                    Document Ingestion
                    Tool: python-docx
                    Input: data/raw/*.docx
                    Output: cleaned document text + source filename metadata
                         |
                         |
                    Chunking
                    Strategy: 500-character chunks with 100-character overlap
                    Output: smaller text chunks with source metadata
                         |
                         |
                    Embedding + Vector Store
                    Embedding Model: sentence-transformers/all-MiniLM-L6-v2
                    Vector Database: ChromaDB
                    Output: searchable vector collection
                         |
                         |
                    Retrieval
                    Method: semantic similarity search
                    Top-k: 4 chunks per query
                    Output: most relevant chunks + citations
                         |
                         |
                    Generation
                    LLM: Groq llama-3.3-70b-versatile
                    Output: grounded answer using only retrieved context

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

**Milestone 3 — Ingestion and chunking:**
I plan to use ChatGPT to help write Python code that loads .docx files from data/raw/ using python-docx. I will give ChatGPT the Documents section and explain that the loader must preserve the filename as metadata for citation. I expect it to produce an ingestion function that returns document text and source metadata.

I will also give ChatGPT my Chunking Strategy section and ask it to implement a chunk_text() function using 500-character chunks and 100-character overlap. I will verify the output by printing the number of chunks and checking a few chunks manually to make sure they are readable and not empty.

**Milestone 4 — Embedding and retrieval:**
I plan to use ChatGPT to help create embedding and ChromaDB indexing code. I will provide the Retrieval Approach section and ask for code using sentence-transformers/all-MiniLM-L6-v2 and ChromaDB. I expect the code to embed each chunk, store it in ChromaDB, and preserve metadata such as source filename and chunk number.

I will verify this by running a few test queries, such as “Is CSC 415 hard?” and checking whether the retrieved chunks come from the CSC 415 Reddit document or Robert Bierman document.

**Milestone 5 — Generation and interface:**
I plan to use ChatGPT to help connect retrieval results to Groq for grounded answer generation. I will provide the Evaluation Plan and ask for a simple command-line interface where a user can type a question and receive an answer with cited sources.

I will verify the output by running the five evaluation questions and checking whether the answer is supported by the retrieved chunks. I will label each result as accurate, partially accurate, or inaccurate in my evaluation report.