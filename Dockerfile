FROM python:3.10

WORKDIR /app

# Copy all project files
COPY . .

# Install backend dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt

# Install Streamlit separately
RUN pip install streamlit

# Expose backend (FastAPI) and frontend (Streamlit) ports
EXPOSE 8000 8501

# Use JSON CMD to avoid warning and run both services
CMD ["bash", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port 8000 & streamlit run frontend/app.py --server.port=8501 --server.address=0.0.0.0 && wait"]
