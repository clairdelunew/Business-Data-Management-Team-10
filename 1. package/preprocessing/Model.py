import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import os
from dotenv import load_dotenv

def load_data(file_path):
    """Load dataset and filter out extreme values."""
    df = pd.read_csv(file_path)
    df = df[df["price_percent_change"] <= 100]
    return df

def preprocess_data(df, features):
    """Extract selected features and standardize them."""
    df_cluster = df[features].dropna()
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df_cluster)
    return df_cluster, df_scaled

def find_optimal_clusters(df_scaled, k_range=(2, 10)):
    """Use Elbow Method and Silhouette Score to determine optimal K."""
    inertia = []
    silhouette_scores = []
    
    for k in range(*k_range):
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(df_scaled)
        inertia.append(kmeans.inertia_)
        silhouette_scores.append(silhouette_score(df_scaled, kmeans.labels_))
    
    return inertia, silhouette_scores

def plot_elbow_silhouette(K_range, inertia, silhouette_scores):
    """Plot the Elbow Method and Silhouette Score graphs."""
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    
    ax[0].plot(K_range, inertia, marker="o", linestyle="-")
    ax[0].set_title("Elbow Method")
    ax[0].set_xlabel("Number of Clusters")
    ax[0].set_ylabel("Inertia")
    
    ax[1].plot(K_range, silhouette_scores, marker="o", linestyle="-", color="red")
    ax[1].set_title("Silhouette Score")
    ax[1].set_xlabel("Number of Clusters")
    ax[1].set_ylabel("Score")
    
    plt.show()

def perform_clustering(df_scaled, df_cluster, df, best_k=4):
    """Perform K-Means clustering and assign labels to the dataset."""
    kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=10)
    df_cluster['Cluster'] = kmeans.fit_predict(df_scaled)
    df['Cluster'] = df_cluster['Cluster'].reindex(df.index)
    return df

def plot_clusters(df):
    """Visualize clustering results."""
    sns.scatterplot(x=df['price_eur'], y=df['price_percent_change'], hue=df['Cluster'], palette="Set1")
    plt.title("K-Means Clustering: Price vs Price Percent Change")
    plt.xlabel("Price (EUR)")
    plt.ylabel("Price Percent Change")
    plt.legend(title="Cluster")
    plt.show()

def print_cluster_summary(df):
    """Print the average price per cluster."""
    print(df.groupby('Cluster')[['price_eur', 'price_before_eur', 'price_percent_change']].mean())

if __name__ == "__main__":
    
    file_path = os.getenv("MODEL_INPUT_PATH")
    print(file_path)
    df = load_data(file_path)
    features = ["price_eur", "price_before_eur", "price_percent_change"]
    df_cluster, df_scaled = preprocess_data(df, features)
    
    K_range = range(2, 10)
    inertia, silhouette_scores = find_optimal_clusters(df_scaled, k_range=(2, 10))
    
    plot_elbow_silhouette(K_range, inertia, silhouette_scores)
    
    best_k = 4  # Select best K based on elbow/silhouette method
    df = perform_clustering(df_scaled, df_cluster, df, best_k=best_k)
    
    plot_clusters(df)
    print_cluster_summary(df)
