from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from rag.config import BASE_DIR, ensure_data_dir
from rag.ingest import ingest_documents
from rag.llm import generate_answer
from rag.retriever import Retriever

app = FastAPI(title="Construction Marketplace Mini RAG")

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
static_dir = BASE_DIR / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

retriever = Retriever(top_k=5)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> Any:
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/ingest")
async def api_ingest() -> Any:
    """Trigger ingestion/building of the vector index."""
    try:
        ensure_data_dir()
        ingest_documents()
        return JSONResponse({"status": "ok", "message": "Documents ingested and index built."})
    except Exception as e:  # noqa: BLE001
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)


@app.post("/api/chat")
async def api_chat(payload: Dict[str, Any]) -> Any:
    question: str = payload.get("question", "")
    mode: str = payload.get("mode", "online")
    if not question.strip():
        return JSONResponse({"status": "error", "message": "Question is required."}, status_code=400)

    try:
        contexts: List[Dict[str, Any]] = retriever.retrieve(question)
        answer = generate_answer(question, contexts, mode=mode)
        return JSONResponse(
            {
                "status": "ok",
                "question": question,
                "mode": mode,
                "contexts": contexts,
                "answer": answer,
            }
        )
    except Exception as e:  # noqa: BLE001
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

