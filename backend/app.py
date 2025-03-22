from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from model import callMe
from pymongo import MongoClient
from bson.objectid import ObjectId
import numpy as np

app = Flask(__name__)
CORS(app)


# Connect to MongoDB Atlas
try:
    db_username = "temp_user"
    db_password = "sVfoK3he1Vc2J7LR"
    connection_string = f"mongodb+srv://{db_username}:{db_password}@cluster0.z2pfe.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(connection_string)
    db = client["Cluster0"]  # Replace "Cluster0" with your database name if different
    collection = db["file_data"]  # Collection named "file_data"
    print("Successfully connected to MongoDB.")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")

from pymongo import MongoClient

def insert_folder_mapping(cluster_id: int, folder_id: str):
    collection = db["folders"]

    # Define the document
    document = {
        "clusterId": cluster_id,
        "folderId": folder_id
    }

    # Insert into the collection
    result = collection.insert_one(document)
    
    print(f"Inserted document ID: {result.inserted_id}")



def fetch_all_embeddings():
    try:
        # Connect to the collection
        collection = db["file_data"]

        # Fetch all documents and extract 'embedding' fields
        cursor = collection.find({}, {"embedding": 1, "_id": 0})
        embeddings = [doc['embedding'] for doc in cursor]

        print(f"Successfully fetched {len(embeddings)} embeddings.")
        return embeddings

    except Exception as e:
        print(f"Error fetching embeddings: {e}")
        return []


@app.route('/', methods=['POST'])
def upload_file():
    try:
        data = request.get_json()

        if not data or 'text' not in data:
            return jsonify({"error": "Invalid request, 'text' field is required"}), 400

        file_content = data['text']
        print("Received text:", file_content)

        file_name = data['file_name']
        print("Received file name:", file_name)

        # get from db later
        curr_embeddings = np.array(fetch_all_embeddings())

        print("FETCHED EMBEDDINGS: ", curr_embeddings)

        labels, kmeans, new_embeddings = callMe([file_content], curr_embeddings)

        print("DONE", new_embeddings)
        curr_data = new_embeddings[-1]
        
        # Create document
        file_document = {
            "name": file_name,
            "embedding": curr_data.tolist()
        }

        # Insert document into MongoDB
        result = collection.insert_one(file_document)
        print(f"Inserted document ID: {result.inserted_id}")


        # pass labels to agent here



        return jsonify({"message": "Data processed and saved"}), 200

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
