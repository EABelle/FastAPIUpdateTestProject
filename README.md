# FastAPIUpdateTestProject

Bootstrap FastAPI project to get updated into latest concepts.

## Overview

This project contains a minimal FastAPI application with a sample `/shipment` endpoint and a Scalar API docs endpoint.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn scalar-fastapi
uvicorn app.main:app --reload
```

Then open:
- http://127.0.0.1:8000/shipment
- http://127.0.0.1:8000/scalar

## Project structure

```text
.
├── app/
│   ├── __init__.py
│   └── main.py
├── .gitignore
├── README.md
└── main.py
```

