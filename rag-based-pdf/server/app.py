import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .rag import load_pdfs_and_index, answer_question

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    import os
    from dotenv import load_dotenv

    # Load environment variables from .env in the project root before importing modules that need them
    PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
    dotenv_path = os.path.join(PROJECT_ROOT, '.env')
    load_dotenv(dotenv_path=dotenv_path)

    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel
    from fastapi.staticfiles import StaticFiles
    from fastapi.middleware.cors import CORSMiddleware
    from .rag import load_pdfs_and_index, answer_question

    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    class Query(BaseModel):
        question: str

    PDF_DIR = os.path.join(PROJECT_ROOT, 'backend', 'pdfs')

    @app.on_event("startup")
    async def startup_event():
        await load_pdfs_and_index(PDF_DIR)

    @app.post("/api/chat")
    async def chat(q: Query):
        if not q.question:
            raise HTTPException(status_code=400, detail="question required")
        return {"answer": await answer_question(q.question)}

    app.mount("/", StaticFiles(directory=os.path.join(PROJECT_ROOT, 'public'), html=True), name="static")
