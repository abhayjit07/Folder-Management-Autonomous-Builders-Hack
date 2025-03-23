from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from model import callMe
from pymongo import MongoClient
from bson.objectid import ObjectId
import numpy as np
from drive import create_subfolder, upload_file_to_drive

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

def insert_folder_mapping(cluster_id: int, folder_id: str, folder_name: str):
    # Connect to the collection
    collection = db["folders"]

    # Define the document
    document = {
        "clusterId": int(cluster_id),
        "folderId": folder_id,
        "folderName": folder_name
    }

    # Insert into the collection
    result = collection.insert_one(document)
    
    print(f"Inserted document ID: {result.inserted_id}")

def fetch_folder_mapping(cluster_id: int):
    collection = db["folders"]

    result = collection.find_one({"clusterId": int(cluster_id)})  # Corrected key
    if result is None:
        print(f"No document found for clusterId: {cluster_id}")
    return result

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

        # save file in local
        file_tmp_name = "tmp_file.txt"
        with open(file_tmp_name, "w") as f:
            f.write(file_content)

        

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
        print("Labels: ", labels)
        cluster_id = labels[-1]
        res = fetch_folder_mapping(cluster_id)
        folder_id = res.get("folderId") if res else None
        print("Folder ID:", folder_id)
        actual_folder_id = folder_id 
        if folder_id is None:
            folder_id = create_subfolder(f"Cluster-{cluster_id}")
            actual_folder_id = folder_id
            insert_folder_mapping(cluster_id, folder_id, f"Cluster-{cluster_id}")

        # Upload file to Google Drive
        file_id = upload_file_to_drive(file_name, file_content, actual_folder_id)
        print("File uploaded with ID:", file_id)

        return jsonify({"message": "Data processed and saved"}), 200

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
