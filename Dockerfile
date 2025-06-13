# 1. Use official Python image
FROM python:3.10

# 2. Set working directory
WORKDIR /app

# 3. Install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the rest of the app code
COPY . .

# 5. Expose FastAPI default port
EXPOSE 8000

# 6. Run the FastAPI app using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
