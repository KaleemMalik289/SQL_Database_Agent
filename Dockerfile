# Use the official lightweight Python image
FROM python:3.10-slim

# Create a non-root user (Required for Hugging Face Spaces)
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

# Set the working directory
WORKDIR /app

# Copy the requirements file from the root
COPY --chown=user:user requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code into the container
COPY --chown=user:user backend/ /app/backend/

# Set the working directory to where main.py lives
WORKDIR /app/backend

# Hugging Face Spaces expose port 7860 by default
EXPOSE 7860

# 1. Generate the synthetic SQLite database
# 2. Boot up the FastAPI server on port 7860
CMD ["sh", "-c", "python app/database/seed/generate_data.py && uvicorn main:app --host 0.0.0.0 --port 7860"]
