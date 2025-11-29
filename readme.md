pip install -r requirements.txt
cp .env.example .env
python -m uvicorn app.main:api --reload