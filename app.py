import os
import subprocess

# 1. Generate the SQLite Database
print("Generating Database...")
subprocess.run(["python", "backend/app/database/seed/generate_data.py"], check=True)

# 2. Start the FastAPI Server on port 7860 (Hugging Face Default)
print("Starting FastAPI Server...")
os.chdir("backend")
os.system("uvicorn main:app --host 0.0.0.0 --port 7860")
