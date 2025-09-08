# Project Setup and Usage

## 1. Create and Activate Virtual Environment
First, set up a virtual environment and install dependencies.

```bash
# Create virtual environment (Linux/macOS)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate   # On Linux/macOS


# Install dependencies from requirements.txt
pip install -r requirements.txt






#Create Database Tables and Load Data
code-->python3 firstTimeData.py





**Run the Application



#Run with SQLite-based data:
uvicorn main2:app --reload

#All the tasks done with JSON can be reviewed by running:
code-->uvicorn main:app --reload
