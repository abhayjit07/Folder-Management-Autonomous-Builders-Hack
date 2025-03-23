# Folder-Management-Autonomous-Builders-Hack

## Project Overview

This project builds an AI-powered agent that organizes files in your Google Drive based on their content. It offers clustering of files into relevant categories using a clean, intuitive interface.

## Features

- **File Upload**: Users can upload files to the AI agent.
- **Content Summarization**: Automatically generate concise summaries using a large language model.
- **File Clustering**: Group similar files using KMeans clustering based on their embeddings.
- **Google Drive Integration**: Organize files into folders using Google Drive API.
- **Database Management**: Maintain organized folder structures in MongoDB.
- **AI Model Integration**: Utilize Gemini API for text processing and content generation.

## Tech Stack

- **Frontend**: React (with Vite)
- **Backend**: Flask (Python)
- **AI Model**: Gemini API
- **Database**: MongoDB Atlas
- **File Storage**: Google Drive API

## Prerequisites

Ensure you have the following installed:

- Node.js and npm
- Python 3.10+
- MongoDB Atlas account
- Google Cloud account (for Google Drive API)
- API key for Gemini AI

## Setup Instructions

### 1. Clone the Repository

```sh
git clone https://github.com/Folder-Management-Autonomous-Builders-Hack.git
cd Folder-Management-Autonomous-Builders-Hack
```

### 2. Backend Setup

```sh
cd backend
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

Configure in the backend folder with the following details:

```ini
MONGO_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net
GOOGLE_API_KEY=your_google_api_key
```

Start the Flask server:

```sh
python app.py
```

### 3. Frontend Setup

```sh
cd ../frontend
npm install
npm run dev
```


## Troubleshooting

### CORS Errors
Ensure Flask CORS is correctly configured in `app.py` using:

```python
from flask_cors import CORS
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})
```

### MongoDB Connection
Double-check your connection string and whitelist your IP in MongoDB Atlas.

### API Key Issues
Confirm that your Gemini API and Google Drive API keys are valid.

## Future Enhancements

- Implement file summarisation features.
- Add file search and retrieval functionalities.
- Visualize clustering results using interactive dashboards.

## Contributors

- **Parikshith**
- **Minank K.P.**
- **Abhayjit Singh Gulati**


