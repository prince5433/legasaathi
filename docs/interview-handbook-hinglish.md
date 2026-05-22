# LegalSaathi Interview Handbook

Ye document tumhare LegalSaathi project ko interview ke liye explain karne ke liye banaya gaya hai. Language simple Hinglish rakhi gayi hai, taaki tum confidently bol sako ki project kya karta hai, andar ka flow kaise kaam karta hai, aur technical decisions kyu liye gaye.

---

## 1. Project Overview

LegalSaathi ek AI-powered legal assistant hai jo Indian legal documents ko simple language me samjhata hai. User PDF ya image upload karta hai jaise rent agreement, FIR, legal notice, court notice, employment contract, etc. System us document ka text extract karta hai, summary banata hai, risky clauses detect karta hai, important dates/deadlines nikalta hai, knowledge graph banata hai, aur user ko document se chat karne deta hai.

### What Problem Does This Project Solve?

India me legal documents aam aadmi ke liye difficult hote hain. Language complex hoti hai, legal clauses confusing hote hain, aur hidden risks easily miss ho jaate hain. Har chhoti cheez ke liye lawyer afford karna bhi possible nahi hota.

LegalSaathi is problem ko solve karta hai:

- Document ko easy Hindi/Hinglish aur English summary me convert karta hai.
- Risky ya unfair clauses highlight karta hai.
- User ko document ke upar direct questions poochhne deta hai.
- Important dates, hearings, notice period, deadlines auto-detect karta hai.
- State-wise law context add karta hai, jaise Maharashtra, Delhi, Karnataka ke rent law differences.
- Template generator se RTI, legal notice, police complaint jaise drafts banata hai.

### Why Was It Built?

Is project ka main goal legal awareness ko accessible banana hai. Normal user ko legal jargon samajhne ke liye expensive consultation ya legal background ki zarurat na pade. Interview me simple answer:

"Maine LegalSaathi isliye build kiya because legal documents usually common people ke liye hard to understand hote hain. Project ka aim AI, RAG, vector search aur graph database use karke document ko readable summary, risk analysis aur conversational Q&A me convert karna hai."

### Real-World Use Case

Example: Ek tenant rent agreement sign karne wala hai. Wo agreement upload karta hai. LegalSaathi batata hai:

- Agreement kis type ka hai.
- Security deposit clause risky hai ya nahi.
- Eviction clause unfair hai ya nahi.
- Notice period kya hai.
- Rent increase clause legal hai ya nahi.
- Maharashtra ya Delhi law ke hisaab se kya implication ho sakta hai.

---

## 2. Tech Stack Breakdown

### Frontend

Frontend Next.js 14 App Router me built hai. React components, TypeScript, Tailwind CSS, Clerk auth UI, Axios, React Dropzone, ReactFlow, d3-force aur lucide-react use hote hain.

Main frontend responsibilities:

- Landing page.
- Dashboard.
- File upload UI.
- Document list.
- Document detail page.
- Summary, risk list, chat, graph, timeline tabs.
- Compare documents page.
- Template generator page.
- Deadlines page.

Important files:

- `frontend/app/page.tsx`: Landing page.
- `frontend/app/dashboard/page.tsx`: Dashboard and upload flow.
- `frontend/app/dashboard/[docId]/page.tsx`: Single document detail page.
- `frontend/app/dashboard/compare/page.tsx`: Document comparison UI.
- `frontend/app/dashboard/templates/page.tsx`: Legal template generator UI.
- `frontend/app/dashboard/deadlines/page.tsx`: Reminder management UI.
- `frontend/lib/api.ts`: Axios client with Clerk token injection.

Why Next.js over normal React?

- Routing built-in hai.
- App Router structure clean hai.
- Production deployment easy hota hai.
- Clerk integration Next.js ke saath smooth hai.
- Future me SSR/server components add karna easy hai.

Why Tailwind over plain CSS?

- Fast UI development.
- Consistent spacing/colors.
- Component-level styling easy.
- No big CSS files maintain karne padte.

### Backend

Backend FastAPI me built hai. Python async backend hai jo file upload, AI analysis, RAG chat, graph, template generation, comparison aur deadline reminders handle karta hai.

Important backend files:

- `backend/main.py`: FastAPI app entrypoint.
- `backend/config.py`: Environment settings.
- `backend/database.py`: MongoDB connection.
- `backend/routes/*.py`: API endpoints.
- `backend/services/*.py`: Business logic and AI/data integrations.
- `backend/middleware/auth.py`: Clerk JWT verification and dev-mode bypass.

Why FastAPI over Flask/Django?

- Async support strong hai.
- API-first backend ke liye lightweight aur fast hai.
- Pydantic validation built-in hai.
- Swagger docs automatically milte hain.
- AI services ke saath async calls easy hain.

### Database

Project me multiple storage systems use hote hain:

1. MongoDB
   - Documents metadata.
   - Extracted raw text.
   - Summary, risks, timeline.
   - Chat history.
   - Deadline reminders.

2. Qdrant
   - Document chunks ke embeddings.
   - Similarity search for RAG.
   - State-law mini knowledge base embeddings.
   - Mem0 vector memory collection.

3. Neo4j
   - Knowledge graph.
   - Document, parties, people, clauses, sections, dates, amounts.
   - Graph visualization and relationship context.

Why MongoDB over SQL?

- Document metadata flexible hai.
- Risks, timeline, messages arrays naturally store ho jaate hain.
- AI output ka structure kabhi-kabhi change hota hai, Mongo flexible schema helpful hai.

Why Qdrant over storing embeddings in MongoDB?

- Vector similarity search ke liye specialized DB hai.
- Cosine distance, metadata filters, scalable search.
- RAG queries fast and relevant banti hain.

Why Neo4j over relational tables?

- Legal documents me relationships important hote hain: party, person, clause, section, date.
- Graph traversal and visualization natural hai.
- Knowledge graph feature ke liye Neo4j best fit hai.

### Authentication

Authentication Clerk se hoti hai.

Frontend Clerk components use karta hai:

- `SignInButton`
- `SignUpButton`
- `UserButton`
- `useAuth().getToken()`

Backend Clerk JWT verify karta hai:

- File: `backend/middleware/auth.py`
- `Authorization: Bearer <token>` header required hota hai jab `DEV_MODE=false`.
- Token RS256 public key se verify hota hai.
- JWT ka `sub` claim user id ke form me use hota hai.

Dev mode:

- `DEV_MODE=true` hone par backend fixed user id `dev_user_001` return karta hai.
- Local testing easy ho jati hai.

### Deployment

Repo local Docker Compose setup use karta hai:

- MongoDB: `localhost:27017`
- Qdrant: `localhost:6333`
- Neo4j: `localhost:7474` browser and `7687` bolt

Backend:

- `uvicorn main:app --reload --port 8000`

Frontend:

- `npm run dev`

Production me possible deployment:

- Frontend: Vercel.
- Backend: Render, Railway, AWS EC2, ECS, or Fly.io.
- MongoDB: MongoDB Atlas.
- Qdrant: Qdrant Cloud.
- Neo4j: Neo4j Aura.
- Files: AWS S3.

### Third-Party APIs

Main APIs/services:

- OpenAI: chat model and embeddings.
- Gemini: fallback LLM.
- Clerk: auth.
- AWS S3: optional file storage.
- SMTP: optional deadline email notifications.
- LangSmith: optional tracing.
- Mem0: user memory.

Why OpenAI primary and Gemini fallback?

- OpenAI has strong chat and embedding models.
- Gemini fallback improves reliability if OpenAI fails.
- LLM provider logic centralized in `llm_service.py`.

---

## 3. Folder Structure Explanation

```text
legalsaathi/
  README.md
  docker-compose.yml
  backend/
    main.py
    config.py
    database.py
    middleware/
    models/
    routes/
    services/
  frontend/
    app/
    components/
    lib/
  mongo_data/
  qdrant_data/
  neo4j_data/
  neo4j_logs/
```

### Root Files

`README.md`

Project setup, architecture, env variables, request flow aur troubleshooting explain karta hai.

`docker-compose.yml`

Local MongoDB, Qdrant aur Neo4j containers start karta hai.

### Backend Folder

`backend/main.py`

FastAPI app yahin create hoti hai. CORS setup, rate limit handler, static files, routes registration, Mongo/Qdrant/Neo4j lifecycle aur deadline scheduler yahin configured hai.

`backend/config.py`

Pydantic settings class. `.env` se config read hota hai, jaise OpenAI key, Mongo URI, Qdrant URL, Clerk keys, SMTP config.

`backend/database.py`

Motor async Mongo client setup karta hai. Helper functions:

- `connect_db()`
- `close_db()`
- `get_documents_col()`
- `get_chats_col()`

`backend/middleware/auth.py`

Clerk JWT verify karta hai. Dev mode me auth bypass hota hai.

`backend/models/`

Pydantic schemas:

- `chat.py`: Chat request/response.
- `document.py`: Document output, doc type enum, risk item.
- `template.py`: Template request/response and template definitions.

`backend/routes/`

API endpoint layer:

- `document.py`: upload/list/get/delete/timeline/compare.
- `chat.py`: ask/stream/history.
- `graph.py`: Neo4j graph APIs.
- `template.py`: legal template APIs.
- `deadline.py`: reminders APIs.
- `jurisdiction.py`: state law APIs.

`backend/services/`

Business logic layer:

- `llm_service.py`: OpenAI/Gemini LLM factory and embeddings.
- `pdf_service.py`: PDF text extraction and image OCR.
- `langgraph_pipeline.py`: ingestion pipeline.
- `qdrant_service.py`: vector storage/search.
- `neo4j_service.py`: entity extraction and graph storage.
- `rag_service.py`: non-streaming RAG answer.
- `rag_service_stream.py`: SSE streaming RAG answer.
- `summarizer_service.py`: summary generation.
- `risk_service.py`: risk detection.
- `classifier_service.py`: document classification.
- `timeline_service.py`: date/deadline extraction.
- `deadline_service.py`: reminder persistence and scheduler job.
- `comparison_service.py`: compare two documents.
- `template_service.py`: generate legal drafts.
- `jurisdiction_service.py`: state-specific law context.
- `memory_service.py`: Mem0 memory.
- `s3_service.py`: S3 or local file upload.
- `relevance_service.py`: checks if question is related to document.

### Frontend Folder

`frontend/app/`

Next.js App Router pages.

`frontend/components/`

Reusable UI and feature components:

- `DocumentUploader.tsx`: Drag-drop upload.
- `ChatInterface.tsx`: Streaming chat UI.
- `KnowledgeGraph.tsx`: ReactFlow graph.
- `DocumentTimeline.tsx`: Timeline UI.
- `DeadlinesWidget.tsx`: Dashboard reminder preview.
- `SummaryCard.tsx`: Summary display.
- `RiskList.tsx`: Risk display.
- `MicButton.tsx`: Voice input.

`frontend/lib/api.ts`

Axios instance banata hai. Clerk token attach karta hai.

---

## 4. Complete Workflow

### User Journey From Start To End

1. User landing page open karta hai.
2. User Clerk se sign in/sign up karta hai.
3. Dashboard pe jaata hai.
4. PDF ya image upload karta hai.
5. Frontend file ko `POST /api/documents/upload` pe bhejta hai.
6. Backend auth verify karta hai.
7. File S3 ya local storage me save hoti hai.
8. PDF text extract hota hai, image ho to vision OCR se text nikalta hai.
9. MongoDB me document `processing` status ke saath insert hota hai.
10. LangGraph pipeline run hoti hai:
    - parse
    - classify
    - chunk
    - embed into Qdrant
    - entity extract
    - store graph in Neo4j
11. Summary, risk detection, classification parallel run hote hain.
12. Mongo document update hota hai with summary, risks, docType, status `done`.
13. Timeline extract hoti hai and reminders create hote hain.
14. Frontend dashboard refresh karta hai.
15. User document detail page kholta hai.
16. User summary, risks, knowledge graph, timeline dekhta hai.
17. User chat me question poochta hai.
18. Backend RAG pipeline Qdrant, Neo4j, Mem0, jurisdiction context use karke answer generate karta hai.
19. Chat history MongoDB me save hoti hai.

### Data Flow: Frontend -> Backend -> DB -> APIs

Upload:

```text
Next.js DocumentUploader
  -> FastAPI /api/documents/upload
  -> Clerk auth
  -> S3/local file storage
  -> PDF/OCR text extraction
  -> MongoDB document insert
  -> LangGraph
      -> Qdrant chunks
      -> Neo4j entities
  -> LLM summary/risk/classification
  -> MongoDB update
  -> response to frontend
```

Chat:

```text
ChatInterface
  -> /api/chat/stream
  -> Mem0 memory search
  -> Mongo document rawText load
  -> Qdrant similarity search
  -> Neo4j related context
  -> State law Qdrant search if selected
  -> relevance classifier
  -> LLM streaming answer
  -> MongoDB chat history
  -> frontend token-by-token UI
```

---

## 5. Architecture

### High-Level System Design

```text
User Browser
  |
  | Next.js UI + Clerk
  v
FastAPI Backend
  |
  |-- MongoDB: documents, chats, reminders
  |-- Qdrant: embeddings and semantic search
  |-- Neo4j: legal/entity graph
  |-- OpenAI/Gemini: AI reasoning
  |-- S3/local: uploaded files
  |-- SMTP: reminder emails
```

### Request-Response Lifecycle

Example upload lifecycle:

1. Browser sends multipart file upload.
2. FastAPI route receives file.
3. Auth dependency returns user id.
4. Backend validates file type and empty file.
5. File saved.
6. Text extracted.
7. Mongo insert creates real ObjectId.
8. LangGraph stores retrieval data.
9. LLM services analyze document.
10. Mongo update saves final output.
11. API returns doc id, summary, risks, doc type.

### State Management

Frontend state mostly React `useState`, `useEffect`, `useCallback` based hai.

Examples:

- Dashboard stores `docs`, `loading`, `confirmDeleteId`.
- Document detail page stores `doc`, `activeTab`, `error`.
- Chat stores `messages`, `input`, `sending`, `language`, `selectedState`.
- Templates page stores wizard step, selected template, form data and generated content.

No Redux/Zustand used because app state mostly page-local hai. Ye interview me explain kar sakte ho:

"Global state library add nahi ki kyunki state sharing complex nahi thi. Auth Clerk handle kar raha hai, API data page-level fetch hota hai, aur chat/upload state component-local hai."

### Component Interaction

Dashboard:

```text
DashboardPage
  -> DocumentUploader
  -> DeadlinesWidget
  -> Document cards
```

Document detail:

```text
DocumentDetailPage
  -> SummaryCard
  -> RiskList
  -> KnowledgeGraph
  -> DocumentTimeline
  -> ChatInterface
```

Chat:

```text
ChatInterface
  -> MicButton
  -> /api/chat/stream
  -> ReactMarkdown render
```

---

## 6. Database Design

### MongoDB Collections

#### `documents`

Approx schema:

```json
{
  "_id": "ObjectId",
  "userId": "clerk_user_id",
  "fileName": "rent.pdf",
  "fileUrl": "/local-files/dev_user_001/rent.pdf",
  "fileType": "application/pdf",
  "rawText": "full extracted document text",
  "status": "processing|done",
  "summary": "LLM generated bilingual summary",
  "risks": [
    {
      "clause": "Security deposit forfeiture",
      "reason": "May be unfair if no clear condition",
      "severity": "high"
    }
  ],
  "docType": "rent|fir|notice|employment|other",
  "timeline": [
    {
      "date": "2026-06-01",
      "event": "...",
      "event_en": "...",
      "type": "deadline",
      "urgency": "important",
      "days_from_now": 10
    }
  ],
  "createdAt": "datetime"
}
```

Why rawText stored?

- Timeline can be regenerated.
- Compare feature needs full text.
- Graph rebuild can happen if Neo4j data missing.
- RAG fallback can use raw text if Qdrant fails.

Trade-off: rawText can be large. Future me encrypted storage or separate blob storage better ho sakta hai.

#### `chats`

```json
{
  "_id": "ObjectId",
  "userId": "clerk_user_id",
  "documentId": "document_object_id",
  "messages": [
    {
      "role": "user",
      "content": "Eviction clause kya hai?",
      "ts": "datetime"
    },
    {
      "role": "assistant",
      "content": "Is agreement me...",
      "ts": "datetime"
    }
  ]
}
```

#### `reminders`

```json
{
  "_id": "ObjectId",
  "userId": "clerk_user_id",
  "documentId": "document_object_id",
  "documentName": "notice.pdf",
  "deadlineDate": "datetime",
  "eventLabel": "Hindi event",
  "eventLabelEn": "English event",
  "eventType": "deadline",
  "urgency": "important",
  "status": "active|dismissed|expired",
  "notificationsSent": {
    "7d": "datetime",
    "3d": "datetime"
  },
  "createdAt": "datetime",
  "updatedAt": "datetime"
}
```

### Qdrant Collections

#### `legal_docs`

Stores document chunks with metadata:

```json
{
  "text": "chunk text",
  "metadata": {
    "doc_id": "document_object_id",
    "doc_type": "rent",
    "chunk_index": 0
  },
  "vector": [1536 dimensional embedding]
}
```

`doc_id` filter important hai taaki user specific document ke against chat kar sake.

#### `state_laws`

Stores state law summaries for jurisdiction-aware answers.

Metadata:

```json
{
  "state": "maharashtra",
  "law_name": "Maharashtra Rent Control Act, 1999",
  "chunk_index": 0
}
```

#### `legalsaathi_mem0`

Mem0 user memory ke liye Qdrant collection use karta hai.

### Neo4j Graph Design

Nodes:

- `Document`
- `Party`
- `Person`
- `Section`
- `Date`
- `Amount`

Relationships:

- `(Document)-[:HAS_PARTY]->(Party)`
- `(Document)-[:MENTIONS]->(Person)`
- `(Document)-[:CITES]->(Section)`
- `(Document)-[:HAS_CLAUSE]->(Section)`
- `(Document)-[:HAS_DATE]->(Date)`
- `(Document)-[:HAS_AMOUNT]->(Amount)`

Why ye design?

- Legal document me relationships very important hote hain.
- Graph visually explain karne se interviewer ko clear impact dikhta hai.
- Neo4j se related context RAG prompt me add hota hai.

### Indexing

Current code me explicit Mongo indexes defined nahi hain. Query patterns:

- `documents`: `userId`, `_id`, `createdAt`
- `chats`: `userId`, `documentId`
- `reminders`: `userId`, `status`, `deadlineDate`

Production improvement:

```text
documents: index on (userId, createdAt)
chats: unique/compound index on (userId, documentId)
reminders: index on (userId, status, deadlineDate)
```

Neo4j improvement:

```cypher
CREATE CONSTRAINT document_id IF NOT EXISTS FOR (d:Document) REQUIRE d.id IS UNIQUE;
CREATE INDEX party_name IF NOT EXISTS FOR (p:Party) ON (p.name);
CREATE INDEX person_name IF NOT EXISTS FOR (p:Person) ON (p.name);
```

---

## 7. Authentication & Security

### JWT / OAuth / Sessions

Clerk handles user authentication. Frontend gets JWT using `getToken()`. Backend receives JWT in:

```text
Authorization: Bearer <token>
```

Backend verifies JWT using Clerk public PEM key and RS256 algorithm.

### Password Hashing

Project itself password store nahi karta. Password hashing Clerk ke side handled hai. Interview me bolna:

"Application passwords directly store nahi karti. Clerk authentication provider password storage, hashing, sessions aur identity management handle karta hai."

### Route Protection

Backend route protection dependency:

```python
user_id: str = Depends(verify_clerk)
```

Har protected route me user id check hota hai. Example:

```python
find_one({"_id": oid, "userId": user_id})
```

Isse ek user doosre user ka document access nahi kar sakta.

Frontend route protection Clerk middleware and Clerk UI se hota hai.

### Current Security Measures

- JWT verification.
- User-scoped Mongo queries.
- File type validation.
- Empty file validation.
- Rate limiting:
  - upload: `10/hour`
  - chat: `20/minute`
  - template generation: `10/hour`
- CORS configured for frontend origins.
- S3 presigned URL support.
- Raw text not returned in list/detail APIs.

### Security Risks + Improvements

Risks:

- Dev mode accidentally production me on reh gaya to auth bypass ho sakta hai.
- Uploaded file size limit explicit nahi dikhta.
- Raw legal text MongoDB me plain text stored hai.
- Local file storage production ke liye secure nahi hai.
- LLM prompt injection possible hai, because document text directly prompt me jaata hai.
- No malware scanning for uploads.
- No explicit audit logs.

Improvements:

- Production me `DEV_MODE=false` enforce karo.
- Upload size limit add karo.
- Raw text encryption at rest add karo.
- S3 private bucket + presigned URLs only.
- Prompt injection guardrails add karo.
- File virus scanning add karo.
- Role-based access and audit logs add karo.
- MongoDB indexes and backups configure karo.

---

## 8. API Breakdown

Base URL local:

```text
http://localhost:8000
```

### Health

`GET /health`

Response:

```json
{
  "status": "ok",
  "version": "6.0.0",
  "dev_mode": true
}
```

### Documents APIs

#### Upload Document

`POST /api/documents/upload`

Form-data:

```text
pdf: file
```

Accepted:

- PDF
- PNG
- JPG/JPEG
- WEBP

Response:

```json
{
  "docId": "665...",
  "fileName": "rent.pdf",
  "fileUrl": "/local-files/dev_user_001/rent.pdf",
  "fileType": "application/pdf",
  "summary": "## Hindi Summary...",
  "risks": [],
  "docType": "rent",
  "status": "done"
}
```

Errors:

- `400`: invalid file type or empty file.
- `422`: text extract nahi ho paya.
- Rate limit: 10/hour.

#### List Documents

`GET /api/documents/list`

Response:

```json
[
  {
    "_id": "665...",
    "userId": "user_123",
    "fileName": "rent.pdf",
    "fileUrl": "/local-files/...",
    "fileType": "application/pdf",
    "summary": "...",
    "risks": [],
    "docType": "rent",
    "status": "done",
    "createdAt": "..."
  }
]
```

#### Get Single Document

`GET /api/documents/{doc_id}`

Returns document metadata without `rawText`.

#### Delete Document

`DELETE /api/documents/{doc_id}`

Deletes:

- Mongo document.
- Chat history.
- Deadline reminders.
- Qdrant chunks.
- Neo4j graph nodes connected to document.

Response:

```json
{
  "deleted": true,
  "docId": "665..."
}
```

#### Timeline

`GET /api/documents/{doc_id}/timeline`

Response:

```json
{
  "events": [
    {
      "date": "2026-06-10",
      "event": "Notice ka deadline",
      "event_en": "Notice deadline",
      "type": "deadline",
      "urgency": "important",
      "days_from_now": 19
    }
  ]
}
```

#### Compare Documents

`POST /api/documents/compare`

Request:

```json
{
  "doc_id_1": "original_doc_id",
  "doc_id_2": "updated_doc_id"
}
```

Response:

```json
{
  "doc1": {"id": "...", "fileName": "old.pdf"},
  "doc2": {"id": "...", "fileName": "new.pdf"},
  "added": [],
  "removed": [],
  "modified": [],
  "new_risks": [],
  "verdict": "Hindi assessment",
  "verdict_en": "English assessment",
  "risk_score_change": "same"
}
```

### Chat APIs

#### Ask Non-Streaming

`POST /api/chat/ask`

Request:

```json
{
  "question": "Eviction clause kya hai?",
  "documentId": "665...",
  "language": "hindi",
  "state": "maharashtra"
}
```

Response:

```json
{
  "answer": "Is document ke hisaab se...",
  "language": "hindi"
}
```

#### Streaming Chat

`POST /api/chat/stream`

Returns Server-Sent Events:

```text
data: {"type":"status","message":"Qdrant mein dhundh raha hoon..."}

data: {"type":"token","content":"Is agreement me"}

data: {"type":"done","full_answer":"Full answer here"}
```

Frontend streaming endpoint first try karta hai. Agar fail ho jaye, fallback `/api/chat/ask` pe jaata hai.

#### Chat History

`GET /api/chat/history/{document_id}`

Response:

```json
{
  "messages": [
    {"role": "user", "content": "...", "ts": "..."},
    {"role": "assistant", "content": "...", "ts": "..."}
  ]
}
```

### Graph APIs

`GET /api/graph/{doc_id}`

Response:

```json
{
  "nodes": [
    {"id": "doc_665", "type": "document", "label": "RENT Document", "connections": 4}
  ],
  "edges": [
    {"source": "doc_665", "target": "party_Ram", "label": "HAS_PARTY"}
  ]
}
```

`GET /api/graph/user/all`

Returns full graph across documents.

### Template APIs

`GET /api/templates/types`

Returns available templates:

- RTI
- Rent notice
- Consumer complaint
- Police complaint
- Legal notice

`POST /api/templates/generate`

Request:

```json
{
  "template_type": "rti",
  "language": "hindi",
  "fields": {
    "applicant_name": "Amit",
    "authority_name": "Municipal Office",
    "information_requested": "..."
  }
}
```

Response:

```json
{
  "template_type": "rti",
  "title": "RTI आवेदन",
  "content": "Markdown legal draft",
  "language": "hindi"
}
```

### Deadline APIs

`GET /api/deadlines`

Upcoming reminders.

`GET /api/deadlines/all`

All reminders including expired/dismissed.

`POST /api/deadlines/{reminder_id}/dismiss`

Dismiss reminder.

`DELETE /api/deadlines/{reminder_id}`

Delete reminder.

`POST /api/deadlines/run-now`

Manually run scheduler job.

`POST /api/deadlines/test-email`

Send test email if SMTP configured.

`GET /api/deadlines/health`

Notifier status.

### Jurisdiction APIs

`GET /api/jurisdiction/states`

Returns available states.

`GET /api/jurisdiction/detect/{doc_id}`

Detects document jurisdiction from raw text.

---

## 8A. Local URLs, Swagger Buttons And Demo Commands

Ye section practical demo ke liye hai. Jab interviewer ya tum khud project run karke check karna chaho, ye URLs aur commands kaam aayenge.

### Start Data Stores

Project root se:

```bash
docker compose up -d
```

Ye three services start karega:

- MongoDB
- Qdrant
- Neo4j

Docker containers check:

```bash
docker ps
```

### Start FastAPI Backend

```bash
cd backend
uvicorn main:app --reload --port 8000
```

Backend health check:

```text
http://localhost:8000/health
```

Expected:

```json
{
  "status": "ok",
  "version": "6.0.0",
  "dev_mode": true
}
```

FastAPI Swagger UI:

```text
http://localhost:8000/docs
```

Ye backend ka manual testing dashboard hai. Yahin se `Try it out` and `Execute` button use karke APIs manually test kar sakte ho.

### Start Frontend

```bash
cd frontend
npm run dev
```

Frontend URL:

```text
http://localhost:3000
```

Dashboard:

```text
http://localhost:3000/dashboard
```

### Open Qdrant

Qdrant dashboard:

```text
http://localhost:6333/dashboard
```

Qdrant collections check:

```bash
curl http://localhost:6333/collections
```

Legal document vector collection check:

```bash
curl http://localhost:6333/collections/legal_docs
```

Interview/demo explanation:

"Agar `legal_docs` collection me `points_count` greater than 0 hai, iska matlab uploaded documents ke chunks embeddings ke saath Qdrant me store ho rahe hain."

### Open Neo4j

Neo4j Browser:

```text
http://localhost:7474
```

Login:

```text
Username: neo4j
Password: reform-william-center-vibrate-press-5829
```

Document nodes check:

```cypher
MATCH (d:Document) RETURN d LIMIT 10;
```

Graph relationships check:

```cypher
MATCH (d:Document)-[r]->(n)
RETURN d, r, n
LIMIT 50;
```

Interview/demo explanation:

"Agar Neo4j me Document node aur related Party, Person, Section, Date, Amount nodes dikh rahe hain, iska matlab knowledge graph pipeline properly kaam kar rahi hai."

### MongoDB Check

Mongo shell open:

```bash
docker exec -it legalsaathi_mongo mongosh -u admin -p admin
```

Database select:

```javascript
use legalsaathi
```

Documents check:

```javascript
db.documents.find().pretty()
```

Chats check:

```javascript
db.chats.find().pretty()
```

Reminders check:

```javascript
db.reminders.find().pretty()
```

### FastAPI Swagger Manual Buttons

Open:

```text
http://localhost:8000/docs
```

Important buttons:

- `GET /health`: backend running hai ya nahi.
- `POST /api/documents/upload`: PDF/image upload test.
- `GET /api/documents/list`: uploaded docs list.
- `GET /api/documents/{doc_id}`: single doc detail.
- `GET /api/documents/{doc_id}/timeline`: timeline extraction check.
- `POST /api/documents/compare`: two docs compare.
- `POST /api/chat/ask`: non-streaming chat check.
- `POST /api/chat/stream`: streaming chat endpoint.
- `GET /api/chat/history/{document_id}`: saved chat history.
- `GET /api/graph/{doc_id}`: Neo4j graph response.
- `GET /api/templates/types`: templates list.
- `POST /api/templates/generate`: legal draft generation.
- `GET /api/deadlines/health`: deadline notifier status.
- `GET /api/deadlines`: upcoming reminders.
- `GET /api/deadlines/all`: all reminders.
- `POST /api/deadlines/run-now`: manually deadline scheduler run.
- `POST /api/deadlines/test-email`: SMTP email test.
- `GET /api/jurisdiction/states`: available state laws.
- `GET /api/jurisdiction/detect/{doc_id}`: state detection.

### Deadline Proper Work Kar Raha Hai Ya Nahi

FastAPI Swagger me ye flow follow karo:

1. Open:

```text
http://localhost:8000/docs
```

2. `GET /api/deadlines/health` execute karo.

Expected:

```json
{
  "enabled": true,
  "smtpConfigured": true,
  "intervalHours": 6,
  "lookaheadDays": 30
}
```

`smtpConfigured: true` ka matlab email sending configured hai. Agar `false` hai, reminder DB me ban sakta hai but email send nahi hoga.

3. Test email bhejne ke liye:

```text
POST /api/deadlines/test-email
```

Expected:

```json
{
  "sent": true,
  "to": "your_email@gmail.com"
}
```

4. Kisi document me future date ke saath upload test karo. Example text/document me aisa deadline ho:

```text
The tenant must vacate the property by 30 June 2026.
Payment must be completed before 15 July 2026.
```

5. Upload ke baad:

```text
GET /api/deadlines
```

Expected:

```json
{
  "items": [
    {
      "_id": "...",
      "documentId": "...",
      "documentName": "...",
      "deadlineDate": "2026-06-30T00:00:00+00:00",
      "eventLabelEn": "...",
      "status": "active",
      "daysRemaining": 39
    }
  ],
  "count": 1
}
```

6. Manual scheduler run:

```text
POST /api/deadlines/run-now
```

Expected:

```json
{
  "summary": {
    "checked": 1,
    "emails_sent": 0,
    "expired": 0,
    "by_window": {}
  },
  "ranAt": "..."
}
```

Meaning:

- `checked`: kitne active reminders scan hue.
- `emails_sent`: kitne emails send hue.
- `expired`: kitne past deadlines expired mark hue.
- `by_window`: `7d`, `3d`, `1d`, `due` window me email send count.

### Reminder Email Change Karna

Receiver email change karna ho, aur `DEV_MODE=true` hai, backend `.env` me:

```env
DEV_EMAIL=new_receiver_email@gmail.com
```

Sender email change karna ho:

```env
SMTP_USER=new_sender@gmail.com
SMTP_PASSWORD=gmail_app_password
SMTP_FROM=LegalSaathi <new_sender@gmail.com>
```

Gmail ke liye normal password nahi chalega. Gmail App Password use karna padega.

Change ke baad backend restart karo:

```bash
cd backend
uvicorn main:app --reload --port 8000
```

Phir Swagger me:

```text
POST /api/deadlines/test-email
```

Execute karke verify karo.

---

## 9. Core Features Deep Dive

### Feature 1: Document Upload and Analysis

Frontend component: `DocumentUploader.tsx`

Backend route: `routes/document.py`

How it works:

- User file drop karta hai.
- File FormData me `/api/documents/upload` pe bheji jaati hai.
- Backend file type validate karta hai.
- PDF ke liye `pdfplumber` text extract karta hai.
- Image ke liye vision model OCR karta hai.
- File S3 ya local folder me store hoti hai.
- MongoDB me initial document insert hota hai.
- LangGraph ingestion pipeline run hoti hai.
- Summary, risks, classification parallel run hote hain.
- Timeline and reminders create hote hain.

Important design decision:

Mongo insert pipeline se pehle hota hai, taaki real `ObjectId` available ho. Is id ko Qdrant metadata aur Neo4j document node me use kiya jaata hai.

### Feature 2: Summary Generation

File: `services/summarizer_service.py`

Logic:

- LLM ko raw text ka first 4000 chars diya jaata hai.
- Prompt asks bilingual summary:
  - Hindi Summary
  - English Summary
- 5 bullet points simple language me return karne ko kaha gaya hai.

Challenge:

LLM kabhi extra text add kar sakta hai. Prompt strict format use karta hai.

### Feature 3: Risk Detection

File: `services/risk_service.py`

Logic:

- LLM risky/unfair clauses detect karta hai.
- JSON output required hota hai.
- Each risk has:
  - clause
  - reason
  - severity
- JSON parse fail ho to empty list return hoti hai.

Why structured JSON?

Frontend risk cards easily render kar sake. Severity ke basis pe colors show kar sake.

### Feature 4: Document Classification

File: `services/classifier_service.py`

Types:

- rent
- fir
- notice
- employment
- other

Logic:

- LLM se exactly one word response manga jaata hai.
- Code first valid token pick karta hai.

### Feature 5: RAG Chat

Files:

- `services/rag_service.py`
- `services/rag_service_stream.py`
- `services/rag_context.py`

RAG means Retrieval Augmented Generation. Sirf LLM se answer generate nahi hota; pehle relevant context retrieve hota hai.

Context sources:

- Mem0: past user memory.
- MongoDB: raw document text.
- Qdrant: semantically relevant document chunks.
- Neo4j: related legal entities.
- Qdrant state laws: jurisdiction context.

Flow:

1. User question.
2. Memory lookup.
3. Document load.
4. Qdrant similarity search.
5. Neo4j related context.
6. State law context if selected.
7. Relevance classifier checks if question related hai.
8. Prompt build hota hai.
9. LLM answer stream karta hai.
10. Memory and Mongo chat history update hota hai.

Why relevance classifier?

Taaki user unrelated questions na pooche, jaise "movie recommend karo". LegalSaathi document-grounded answer hi de.

### Feature 6: Streaming Chat

Backend endpoint: `/api/chat/stream`

Frontend: `ChatInterface.tsx`

How it works:

- Backend async generator SSE events bhejta hai.
- Status messages first aate hain.
- LLM tokens one-by-one stream hote hain.
- Frontend `fetch` reader se chunks read karta hai.
- UI me assistant message gradually update hota hai.

Why streaming?

Long LLM answers me user ko wait karna boring hota hai. Streaming se perceived speed improve hoti hai.

### Feature 7: Knowledge Graph

Backend:

- `services/neo4j_service.py`
- `routes/graph.py`

Frontend:

- `KnowledgeGraph.tsx`

How it works:

- LLM document text se entities extract karta hai.
- Entities JSON me aati hain.
- Neo4j me Document node and related nodes create hote hain.
- Graph API nodes/edges return karta hai.
- ReactFlow graph render karta hai.
- d3-force layout graph positions calculate karta hai.

Why knowledge graph?

Legal document me parties, clauses, dates, sections interconnected hote hain. Graph se interviewer ko advanced architecture dikhta hai.

### Feature 8: Timeline and Deadline Reminders

Files:

- `timeline_service.py`
- `deadline_service.py`
- `routes/deadline.py`
- `DocumentTimeline.tsx`
- `DeadlinesWidget.tsx`

How it works:

- LLM dates/deadlines extract karta hai.
- Events Mongo document me cache hote hain.
- Future events `reminders` collection me store hote hain.
- APScheduler periodically `process_due_reminders()` run karta hai.
- 7d, 3d, 1d, due date windows pe email send hota hai if SMTP configured.

Why useful?

Legal documents me deadlines miss karna costly hota hai. This feature real-world value add karta hai.

### Feature 9: Document Comparison

File: `comparison_service.py`

How it works:

- User two documents select karta hai.
- Backend rawText load karta hai.
- LLM compare karta hai:
  - added clauses
  - removed clauses
  - modified clauses
  - new risks
  - verdict
  - risk score change

Use case:

Agreement ka old vs new version compare karna.

### Feature 10: Legal Template Generator

Files:

- `models/template.py`
- `services/template_service.py`
- `routes/template.py`
- `dashboard/templates/page.tsx`

Supported templates:

- RTI Application
- Rent Notice
- Consumer Complaint
- Police Complaint
- Legal Notice

How it works:

- Frontend template fields render karta hai.
- Required fields validate hote hain.
- Backend LLM prompt se legal draft generate karta hai.
- Frontend markdown preview and print-to-PDF support karta hai.

### Feature 11: Jurisdiction-Aware Answers

File: `jurisdiction_service.py`

How it works:

- App top Indian states ke rent/legal summaries store karta hai.
- On app startup, state laws Qdrant collection me indexed hote hain.
- User chat me state select kar sakta hai.
- RAG answer me state-specific legal context inject hota hai.

Interview line:

"Normal RAG document tak limited hota hai. Maine jurisdiction layer add ki, jisme selected Indian state ke legal rules vector-search hoke answer me include hote hain."

---

## 10. Important Code Explanation

### `backend/main.py`

Role:

- FastAPI app create karta hai.
- Lifespan me Mongo connect, Qdrant init, state law collection init hota hai.
- Deadline scheduler start hota hai.
- CORS setup hota hai.
- Routes include hote hain.
- `/local-files` mount hota hai.

Important:

```python
app.include_router(document_routes.router, prefix="/api/documents")
app.include_router(chat_routes.router, prefix="/api/chat")
```

### `backend/routes/document.py`

Most important route: `upload_document`

Key points:

- File type validation.
- File bytes read once.
- File storage.
- Text extraction.
- Mongo insert before pipeline.
- LangGraph pipeline.
- Parallel LLM analysis with `asyncio.gather`.
- Timeline extraction.
- Deadline registration.

### `backend/services/langgraph_pipeline.py`

Pipeline:

```text
parse -> classify -> chunk -> extract_entities
```

Why LangGraph?

- Pipeline state clearly pass hota hai.
- Future me conditional branching easy hai.
- AI ingestion workflow modular hota hai.

### `backend/services/qdrant_service.py`

Role:

- Qdrant collection create karta hai.
- Chunks store karta hai.
- Similarity search karta hai.
- Delete document chunks.

Embedding dimension `1536` hai because `text-embedding-3-small` model use hota hai.

### `backend/services/neo4j_service.py`

Role:

- LLM se entities JSON extract.
- Neo4j me nodes and relationships create.
- RAG ke liye related context return.

### `backend/services/rag_service_stream.py`

Role:

- Streaming answer generate karta hai.
- SSE status events bhejta hai.
- Retrieval context gather karta hai.
- LLM token stream karta hai.

### `frontend/lib/api.ts`

Role:

- Axios client create.
- API base URL set.
- Clerk JWT attach.

Interview line:

"API client centralized hai, isliye har component me auth header manually add nahi karna padta."

### `frontend/components/ChatInterface.tsx`

Role:

- Chat history fetch.
- State dropdown load.
- SSE stream read.
- Token by token assistant message update.
- Fallback to non-streaming API if streaming fails.

### `frontend/components/KnowledgeGraph.tsx`

Role:

- Graph API se nodes/edges fetch.
- d3-force se layout.
- ReactFlow se interactive graph render.
- Fullscreen, fit view, relayout controls.

---

## 11. Scalability & Optimization

### Current Performance Bottlenecks

- LLM calls slow and expensive ho sakte hain.
- Upload route heavy hai because same request me extraction, embedding, graph, summary, risks sab run hote hain.
- Raw text large documents ke liye prompt truncation hota hai.
- Mongo indexes missing hain.
- Neo4j entity extraction full LLM based hai, cost high ho sakti hai.
- Chat history array grow karta rahega.
- No background job queue currently.

### Current Optimizations

- Summary, risk, classification parallel run hote hain via `asyncio.gather`.
- Qdrant vector search sirf relevant chunks retrieve karta hai.
- Raw text API response me return nahi hota.
- Timeline cache Mongo document me stored hota hai.
- Streaming chat perceived latency reduce karta hai.
- Rate limiting abuse control karta hai.

### Caching

Current caching:

- LLM and embeddings objects `lru_cache` se reuse hote hain.
- Timeline document me cache hoti hai.
- State laws Qdrant me once indexed hote hain.

Future caching:

- Summary/risk regeneration cache.
- Redis for recent chat context.
- Redis rate limiting.
- CDN for static file access.

### Lazy Loading

Frontend me graph and timeline tab data tab open hone par component load ke through fetch hota hai. Dashboard initial load sirf docs list fetch karta hai.

Future:

- Dynamic import for heavy graph component.
- Paginate document list.
- Infinite scroll chat history.

### DB Optimization

Mongo:

- Compound indexes add karo.
- Chat messages paginate karo.
- Raw text separate collection ya encrypted blob me store karo.

Qdrant:

- Metadata indexing for `doc_id`.
- Batch embedding for large docs.
- Chunk size tune karna.

Neo4j:

- Unique constraints.
- Batch writes instead of many separate queries.
- User id attach to graph nodes for stronger isolation.

### Future Scaling

Better production architecture:

```text
Frontend
  -> API Gateway / FastAPI
  -> Job Queue (Celery/RQ/Cloud Tasks)
  -> Worker for document processing
  -> MongoDB Atlas
  -> Qdrant Cloud
  -> Neo4j Aura
  -> S3
  -> Redis cache
```

Main improvement:

Upload should return quickly with status `processing`. Background worker should process document asynchronously.

---

## 12. Challenges & Trade-offs

### Trade-off 1: MongoDB vs PostgreSQL

MongoDB chosen because AI outputs flexible hain. Risks, timeline, messages nested arrays me store karna simple hai.

Alternative PostgreSQL hota to relational consistency stronger hoti, but schema changes and nested AI output thoda harder hota.

### Trade-off 2: Multi-Database Architecture

Project MongoDB + Qdrant + Neo4j use karta hai.

Pros:

- Har DB apne use case me best hai.
- RAG quality better.
- Graph feature strong.

Cons:

- Operational complexity badh jaati hai.
- Data consistency manage karni padti hai.
- Delete operation me multiple systems clean karne padte hain.

### Trade-off 3: LLM-Based Extraction

Pros:

- Fast development.
- Works across document formats.
- Flexible for legal language.

Cons:

- Output sometimes inconsistent.
- JSON parse failures possible.
- Cost and latency.
- Hallucination risk.

### Trade-off 4: Synchronous Upload Processing

Pros:

- Simpler implementation.
- User gets result immediately after upload.

Cons:

- Long request time.
- Timeout risk.
- Large documents can slow API.

Better alternative:

- Background job queue.
- Websocket/SSE status updates.

### Trade-off 5: Clerk Auth

Pros:

- Secure auth quickly.
- Password handling outsourced.
- JWT integration easy.

Cons:

- Third-party dependency.
- Pricing/vendor lock-in.

Alternative:

- NextAuth/Auth.js
- Custom JWT auth
- Firebase Auth

---

## 13. Possible Interview Questions

### Beginner Questions

Q: LegalSaathi kya karta hai?

A: LegalSaathi ek AI legal assistant hai jo legal documents upload karke summary, risk detection, timeline, reminders, knowledge graph aur document-based chat provide karta hai.

Q: Frontend kis framework me hai?

A: Next.js 14 App Router with React, TypeScript and Tailwind CSS.

Q: Backend kis framework me hai?

A: FastAPI, because async APIs, Pydantic validation and Swagger docs built-in milte hain.

Q: Database kya use kiya?

A: MongoDB for app data, Qdrant for vector search, Neo4j for knowledge graph.

Q: Authentication kaise hoti hai?

A: Clerk se. Frontend JWT leta hai, backend RS256 public key se token verify karta hai.

### Intermediate Questions

Q: RAG kaise kaam karta hai?

A: User question ke liye Qdrant se relevant chunks milte hain, Neo4j se related entities milti hain, Mem0 se past context milta hai, optional state-law context add hota hai, phir LLM answer generate karta hai.

Q: Qdrant ka role kya hai?

A: Document chunks ke embeddings store karta hai. Chat ke time semantic similarity search se relevant chunks retrieve karta hai.

Q: Neo4j kyu use kiya?

A: Legal entities aur relationships graph form me natural hain. Parties, clauses, sections, dates ka relation show karne ke liye Neo4j suitable hai.

Q: Upload ke time Mongo insert pehle kyu hota hai?

A: Real ObjectId chahiye hota hai, jisse Qdrant chunks aur Neo4j nodes same doc id se linked rahein. Temporary id use karne se mismatch bugs aa sakte hain.

Q: Streaming chat kaise implement hai?

A: Backend SSE events stream karta hai, frontend fetch reader se chunks read karta hai and assistant message incrementally update karta hai.

### Advanced Questions

Q: Is architecture me consistency issue kaise handle karoge?

A: Currently delete route Mongo, chats, reminders, Qdrant and Neo4j cleanup karta hai. Production me background jobs, retries, idempotent operations and transactional outbox pattern use karunga.

Q: LLM hallucination kaise reduce karte ho?

A: RAG context provide karta hoon, relevance classifier use karta hoon, prompt document-grounded answer ke liye build hota hai. Future me citations, chunk references, confidence score and answer refusal improve karunga.

Q: Large document upload kaise scale karoge?

A: Upload ko async background job me shift karunga. Chunking and embeddings worker process karega. Frontend polling/SSE se status show karega. File direct S3 presigned upload se backend bandwidth reduce hogi.

Q: Security improvements kya karoge?

A: Dev mode production me disable, upload size limit, file scanning, encryption at rest, stricter CORS, audit logs, prompt injection filters and user-level graph isolation.

Q: Why not use only MongoDB?

A: MongoDB app data ke liye good hai, but vector search and graph traversal ke liye specialized databases better hain. Qdrant semantic search optimize karta hai, Neo4j relationships optimize karta hai.

### "Why Did You Choose X Over Y?"

Q: FastAPI over Django?

A: Project API-heavy and AI-heavy hai. FastAPI async, lightweight and Pydantic-friendly hai. Django full-stack MVC ke liye better hota, but yahan separate Next.js frontend hai.

Q: Qdrant over Pinecone?

A: Qdrant self-host locally Docker me easy hai, open-source hai, metadata filtering support karta hai. Pinecone managed service hai but local development and cost ke liye Qdrant better fit tha.

Q: Clerk over custom auth?

A: Auth security sensitive hota hai. Clerk se auth, sessions, JWT, password handling quickly reliable mil gaya. Custom auth build karne me security risk aur time zyada hota.

Q: MongoDB over PostgreSQL?

A: AI-generated nested data flexible hai. MongoDB me documents, risks, timeline, chat arrays natural fit hain.

Q: LangGraph kyu?

A: Document ingestion multiple steps ka workflow hai. LangGraph se parse, classify, chunk, entity extraction modular graph pipeline me organize hota hai.

---

## 14. How To Explain This Project In Interview

### 30 Sec Answer

"LegalSaathi ek AI-powered legal document assistant hai. User rent agreement, FIR, notice ya contract upload karta hai, aur system uska text extract karke simple Hindi-English summary, risky clauses, important deadlines, knowledge graph aur document-based chat provide karta hai. Frontend Next.js me hai, backend FastAPI me, MongoDB app data ke liye, Qdrant RAG vector search ke liye, Neo4j knowledge graph ke liye, aur Clerk authentication ke liye use kiya hai."

### 2 Min Answer

"LegalSaathi ka goal legal documents ko common users ke liye understandable banana hai. User PDF ya image upload karta hai. Backend file validate karta hai, PDF se text extract karta hai ya image ke liye OCR use karta hai. Document MongoDB me store hota hai. LangGraph pipeline document ko classify karti hai, chunks banati hai, embeddings Qdrant me store karti hai, aur LLM se entities extract karke Neo4j graph me store karti hai. Parallel me summary, risk detection aur document classification run hota hai. User detail page par summary, risk list, graph, timeline aur chat dekh sakta hai. Chat RAG-based hai: Qdrant se relevant chunks, Neo4j se entity context, Mem0 se user memory, aur state-law context combine karke LLM answer generate karta hai. Project me Clerk auth, rate limiting, deadline reminders, template generation and document comparison bhi hai."

### Deep Technical Explanation

"Architecture me frontend Next.js App Router hai and backend FastAPI. Auth Clerk JWT se hota hai; frontend token attach karta hai and backend RS256 public key se verify karta hai. Upload route multipart file receive karta hai. PDF extraction pdfplumber se hoti hai and image OCR vision model se hota hai. MongoDB me document first insert hota hai so we get real ObjectId. Ye ObjectId Qdrant metadata and Neo4j Document node me use hota hai. LangGraph pipeline parse, classify, chunk/embed and entity extraction nodes run karti hai. Qdrant collection legal_docs me chunk embeddings store hote hain using OpenAI text-embedding-3-small. Neo4j me parties, persons, sections, clauses, dates and amounts store hote hain. Chat endpoint streaming SSE use karta hai. It collects memory, vector search result, graph context and jurisdiction context, then relevance classifier ensures question document-related hai. LLM provider abstraction OpenAI primary and Gemini fallback rakhta hai. MongoDB stores documents, chat history and reminders. APScheduler periodically reminders scan karta hai and SMTP configured ho to emails send karta hai."

---

## 15. Weak Points / Improvements

### Current Limitations

- Upload processing synchronous hai.
- Explicit MongoDB indexes missing.
- Large files ke liye timeout risk.
- LLM output validation limited hai.
- Raw text plain MongoDB me stored hai.
- No automated test suite visible in repo.
- No CI/CD configured.
- No dedicated background worker.
- Prompt injection handling basic hai.
- Legal accuracy needs citations and disclaimers.
- Graph data user-specific isolation Neo4j level pe stronger ho sakti hai.

### Architecture Improvements

- Background job queue add karo.
- Upload status API add karo.
- Redis cache and queue add karo.
- Direct-to-S3 presigned upload.
- Better document parser for scanned PDFs.
- Chunk citations return karo.
- Multi-tenant graph model improve karo.
- Structured LLM output with stricter schema validation.
- Observability with LangSmith and app logs.

### Security Improvements

- Production config validation.
- `DEV_MODE=false` enforce in production.
- File size limit.
- Virus scanning.
- Raw text encryption.
- Data retention policy.
- Audit logs.
- Prompt injection detection.
- Stronger CORS origin config.

### Better Scaling Options

- MongoDB Atlas.
- Qdrant Cloud.
- Neo4j Aura.
- Workers on Celery/RQ.
- Redis for jobs and cache.
- Separate AI worker service.
- API gateway and autoscaling.
- CDN for frontend and static assets.

---

## 16. Resume Worthy Impact

Strong resume bullets:

- Built an AI-powered legal document assistant using Next.js, FastAPI, MongoDB, Qdrant, Neo4j and OpenAI to simplify Indian legal documents into summaries, risk flags and conversational Q&A.
- Implemented a RAG pipeline with vector search, graph context, user memory and jurisdiction-aware legal context for document-grounded answers.
- Designed multi-database architecture using MongoDB for app data, Qdrant for semantic retrieval, and Neo4j for legal knowledge graph visualization.
- Added streaming chat using Server-Sent Events, improving perceived response latency for long AI answers.
- Built document intelligence features including risk detection, bilingual summaries, timeline extraction, deadline reminders, document comparison and legal template generation.
- Integrated Clerk JWT authentication, rate limiting, S3/local file storage fallback and scheduled email reminders.

Short resume version:

"Developed LegalSaathi, an AI legal assistant that analyzes Indian legal documents using RAG, vector search and knowledge graphs; delivered bilingual summaries, risk detection, timeline reminders, document comparison and streaming chat with Next.js, FastAPI, MongoDB, Qdrant, Neo4j and OpenAI."

---

## 17. Mock Viva / Interview Defense

Q: Ye project sirf ChatGPT wrapper hai kya?

A: Nahi. Sirf prompt bhejna nahi ho raha. Project me full document ingestion pipeline hai: PDF/OCR extraction, Mongo storage, chunking, embeddings in Qdrant, entity graph in Neo4j, timeline extraction, reminders, document comparison and template generation. Chat RAG-based hai, jisme retrieved document context, graph context, memory and jurisdiction context combine hota hai.

Q: Agar LLM galat answer de to?

A: Current system RAG se context-grounded answer generate karta hai and relevance classifier unrelated questions block karta hai. Future improvement me citations, exact chunk references, confidence score, legal disclaimer and human review flow add karunga.

Q: Tumne three databases kyu use kiye? Overengineering nahi hai?

A: Is project me three different data access patterns hain. App records ke liye MongoDB, semantic search ke liye Qdrant, relationships and visualization ke liye Neo4j. Agar simple CRUD app hota to overengineering hota, but legal document assistant me RAG and graph features core hain.

Q: Upload route slow hoga. Kya karoge?

A: Yes, current design synchronous hai. Production me upload ke baad Mongo status `processing` return karunga, background worker embeddings and LLM analysis karega, frontend polling/SSE se status update lega.

Q: User A User B ka document access kar sakta hai?

A: Backend har document query me `_id` ke saath `userId` filter use karta hai. JWT se user id nikalta hai. Isse direct object id guess karne par bhi unauthorized document return nahi hoga.

Q: Qdrant me data isolation kaise hai?

A: Chunks metadata me `doc_id` store hota hai. Chat query me `filter={"doc_id": doc_id}` use hota hai. Production me userId metadata bhi add karna better hoga for extra isolation.

Q: Neo4j cleanup kaise hota hai?

A: Document delete route Neo4j me `MATCH (d:Document {id: $doc_id})` karke connected nodes detach delete karta hai and orphan neighbours cleanup karta hai.

Q: Prompt injection risk hai?

A: Haan, legal documents malicious instructions contain kar sakte hain. Current system relevance and document-grounded prompt use karta hai, but future me prompt injection detection, system prompt hardening and output citations add karunga.

Q: Why not use LangChain only, LangGraph kyu?

A: LangChain components services me use ho rahe hain, but ingestion ek multi-step workflow hai. LangGraph workflow state pass karne and steps organize karne ke liye cleaner hai.

Q: Isme legal advice ka risk hai?

A: App legal awareness tool hai, lawyer replacement nahi. Production me clear disclaimer, source citations and "consult a lawyer" warnings add karna zaruri hai.

Q: Agar OpenAI down ho jaye?

A: `llm_service.py` me OpenAI primary hai and Gemini fallback configured hai. Chat and analysis calls `ainvoke_with_fallback` use karte hain.

Q: Deadline reminders kaise kaam karte hain?

A: Timeline service LLM se dates/deadlines extract karta hai. Future events reminders collection me store hote hain. APScheduler every configured interval reminders scan karta hai and 7d/3d/1d/due windows pe SMTP email send karta hai.

Q: State law context hardcoded kyu hai?

A: Current version me state law mini knowledge base seeded hai for top states, taaki jurisdiction-aware RAG demonstrate ho sake. Production me official legal sources, periodic updates and citations add karunga.

Q: Testing strategy kya hogi?

A: Backend unit tests services ke liye, route tests with FastAPI TestClient, mocked LLM responses, integration tests for Mongo/Qdrant/Neo4j using test containers, and frontend component tests for upload/chat flows.

Q: Is project ka sabse technically strong part kya hai?

A: RAG pipeline with multiple context sources: Qdrant semantic retrieval, Neo4j graph context, Mem0 user memory and jurisdiction-aware state law retrieval. Ye simple chatbot se zyada robust document intelligence system banata hai.

---

## 18. Final Interview Pitch

"LegalSaathi ko main ek document intelligence platform ke roop me explain karunga, jiska target Indian legal documents ko aam users ke liye understandable banana hai. Isme Next.js frontend, FastAPI backend, Clerk auth, MongoDB app data, Qdrant vector search, Neo4j knowledge graph and OpenAI/Gemini LLM layer hai. User document upload karta hai, system text extract karke embeddings, graph, summary, risks and timeline generate karta hai. Chat RAG-based hai, jo document chunks, graph entities, user memory and state law context combine karta hai. Project me real-world features hain jaise deadline reminders, comparison, templates and streaming chat. Current limitations me background processing, stronger indexing, citations and security hardening future improvements hain."
