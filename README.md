# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->
This project focuses on SFSU Computer Science student experiences. The system helps users find information about professors, course difficulty, elective requirements, easy classes, and opinions about the SFSU CS program.

This knowledge is valuable because official university resources only provide course descriptions and degree requirements. They do not provide student opinions about workload, teaching quality, grading style, or recommendations for specific professors and courses. Students often rely on unofficial sources such as Reddit and Rate My Professors to make academic decisions.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 |Anthony Souza Reviews| Rate My Professors |data/raw/anthony_souza_rmp.docx
  2 |Duc Ta Reviews |Rate My Professors	|data/raw/duc_ta_rmp.docx
  3 |Jose Ortiz-Costa Reviews	|Rate My Professors	|data/raw/jose_ortiz_costa_rmp.docx
  4 |Matt Pico Reviews |Rate My Professors |data/raw/Matt_pico_rmp.docx
  5 |Robert Bierman Reviews| Rate My Professors| data/raw/robert_bierman_rmp.docx
  6 |Best CS Professors Discussion| Reddit r/SFSU	| data/raw/reddit_best_cs_professors.docx
  7 |CS Elective Requirements Discussion|Reddit r/SFSU	| data/raw/reddit_cs_elective_requirements.docx
  8 |SFSU CS Program Discussion| Reddit r/SFSU| data/raw/reddit_cs_program_sfsu.docx
  9 |CSC 415 Professor Recommendations	|Reddit r/SFSU	| data/raw/reddit_csc415_professor_recommendations.docx
  10 |Easy Classes at SFSU| Reddit r/SFSU| data/raw/reddit_easy_classes_sfsu.docx 
## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**

**Overlap:**

**Why these choices fit your documents:**

**Final chunk count:**

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->
 Chunk size: 350 characters

Overlap: 75 characters

Why these choices fit your documents:

The documents consist primarily of short reviews, Reddit comments, and student discussions. Smaller chunks preserve individual opinions and recommendations without mixing unrelated content. Overlap was added to preserve context when important information appears near chunk boundaries.

Final chunk count: 56 chunks

**Model used:**

Model used: all-MiniLM-L6-v2 via sentence-transformers

**Production tradeoff reflection:**

I selected all-MiniLM-L6-v2 because it is free, lightweight, and runs locally without requiring an API key. It performs well on short opinion-based text such as reviews and Reddit discussions. For a production system, I would evaluate larger embedding models that provide better semantic accuracy, support multilingual text, and handle larger document collections. I would also consider latency, inference cost, and scalability.


---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**
System prompt grounding instruction:

The prompt explicitly instructs the model:

"Answer the user's question using ONLY the provided context. Do not use outside knowledge. If the context does not contain enough information to answer, say: 'I don't have enough information in the provided documents to answer that.'"

A distance threshold was also used to reject weak retrievals before generation.

**How source attribution is surfaced in the response:**

Source attribution is generated programmatically rather than relying on the LLM. After generation, the system displays the source filename, chunk number, and retrieval distance for every retrieved chunk used to answer the question.



---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

Evaluation Report
#	Question	Expected answer	System response (summarized)	Retrieval quality	Response accuracy
1. What do students say about Robert Bierman and CSC 415?	
Students describe CSC 415 as difficult, but Bierman is knowledgeable and organized.	
System reported mixed reviews, noting that Bierman is strict but knowledgeable and organized.	Relevant	Accurate
2. Are CS students required to complete 12 units of electives?	
Yes, 12 units are required.	
System correctly stated that CS majors must complete 12 units of electives.	
Relevant	Accurate
3. What do students say about the SFSU CS program overall?	
Students believe success depends heavily on effort outside coursework.	
System summarized mixed opinions and emphasized projects, internships, and interview preparation.	
Relevant	Accurate
4. Which professor is praised as helpful by students?	
Anthony Souza, Duc Ta, and Jose Ortiz-Costa receive positive reviews.	
System retrieved positive reviews and summarized them, but generalized slightly.	
Relevant	Partially Accurate
5. What do students say about campus parking?	
No information exists in the dataset.	
System declined to answer and stated that the documents did not contain enough information.	
Off-target retrieval but correctly rejected	Accurate

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

**Question that failed:**

Which professor is praised as helpful by students?

**What the system returned:**

The system stated that all professors in the retrieved context were praised as helpful.

**Root cause (tied to a specific pipeline stage):**

The retrieval stage successfully returned relevant professor reviews. However, the generation stage overgeneralized the retrieved information and summarized multiple positive reviews too broadly.

**What you would change to fix it:**

I would strengthen the prompt by requiring the model to explicitly list the professors mentioned in the retrieved chunks rather than generating a general summary. I would also consider retrieving fewer but more focused chunks.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

The planning document helped determine the chunking strategy, retrieval design, evaluation questions, and overall system architecture before coding began. Having these decisions documented made implementation easier and reduced unnecessary changes during development.

**One way your implementation diverged from the spec, and why:**

The original plan used 500-character chunks with 100-character overlap. After inspecting retrieval results, I reduced the chunk size to 350 characters and overlap to 75 characters. This increased the total number of chunks and improved retrieval quality for short review-style documents.

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

- *What I gave the AI:*

My document structure, chunking strategy, and ingestion requirements.

- *What it produced:*

A Python ingestion and chunking pipeline using python-docx.

- *What I changed or overrode:*

I adjusted the chunk size from the original plan and verified the output manually before continuing.

**Instance 2**

- *What I gave the AI:*

My retrieval approach and architecture diagram.

- *What it produced:*

ChromaDB indexing code, retrieval functions, and Groq integration.

- *What I changed or overrode:*

I added a retrieval distance threshold to prevent generation from using weak matches and improved grounding for unsupported questions.