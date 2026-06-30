# ClearCall

A VAR transparency tool that explains contested soccer referee decisions using the official FIFA Laws of the Game.

## What it does

Soccer fans watch VAR overturn goals and award penalties with no real explanation. ClearCall fixes that. Select a real match incident, ask a question in plain English, and get a clear answer pulled directly from the FIFA 2024/25 rulebook, powered by IBM watsonx AI.

## How it works

1. User selects a contested incident from a real match
2. A RAG pipeline retrieves the most relevant rules from the FIFA Laws of the Game (570 chunks indexed in ChromaDB)
3. IBM watsonx generates a plain-English explanation grounded in those rules

## Tech stack

- **Frontend:** React (Vite)
- **Backend:** FastAPI
- **AI:** IBM watsonx (granite-4-h-small)
- **RAG:** ChromaDB + LangChain + official FIFA Laws of the Game PDF
- **Deployment:** Render

## Live demo

- Frontend: https://clearcallsite.onrender.com
- API docs: https://clearcall-x21e.onrender.com/docs

Built for the IBM June Innovation Challenge 2026
