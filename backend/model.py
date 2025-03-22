import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# curr_embeddings = []

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
    

def generate_single_embedding(texts, curr_embeddings, model_name='sentence-transformers/all-mpnet-base-v2'):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)

        # Convert to list if it is not
    if isinstance(curr_embeddings, np.ndarray):
        curr_embeddings = curr_embeddings.tolist()

    for text in texts:
        inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
            sentence_embedding = outputs.last_hidden_state.mean(dim=1).squeeze()
            curr_embeddings.append(sentence_embedding.numpy())

    return np.array(curr_embeddings)

def generate_llm_embeddings(texts, model_name='sentence-transformers/all-mpnet-base-v2'):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)

    embeddings = []
    for text in texts:
        inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
            sentence_embedding = outputs.last_hidden_state.mean(dim=1).squeeze()
            embeddings.append(sentence_embedding.numpy())

    return np.array(embeddings)

def plot_elbow(features):
    wcss = []
    max_clusters = min(len(features), 10)
    for i in range(1, max_clusters + 1):
        kmeans = KMeans(n_clusters=i, random_state=42)
        kmeans.fit(features)
        wcss.append(kmeans.inertia_)
    
    plt.plot(range(1, max_clusters + 1), wcss)
    plt.xlabel('Number of Clusters')
    plt.ylabel('WCSS')
    plt.title('Elbow Method')
    plt.show()

def cluster_documents(features, num_clusters=None):
    if num_clusters is None:
        num_clusters = min(3, len(features))

    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    labels = kmeans.fit_predict(features)
    return labels, kmeans

def main(file_paths):
    texts = [read_file(file_path) for file_path in file_paths]
    embeddings = generate_single_embedding(texts)

    print("Generated embeddings shape:", embeddings.shape)

    # Plot Elbow Method
    plot_elbow(embeddings)

    # Perform Clustering
    labels, kmeans = cluster_documents(embeddings)
    print("Cluster Labels:", labels)

def callMe(text, curr_embeddings = []):

    new_embeddings = generate_single_embedding(text, curr_embeddings)

    # Perform Clustering
    labels, kmeans = cluster_documents(new_embeddings)
    print("Cluster Labels:", labels)
    return [labels, kmeans, new_embeddings]

