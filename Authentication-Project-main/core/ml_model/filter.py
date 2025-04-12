import os
import pandas as pd
import pickle
from sklearn.neighbors import NearestNeighbors
from sklearn.tree import DecisionTreeClassifier

# Set base directory (path of this file)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load athlete dataset
def load_data(csv_path=os.path.join(BASE_DIR, "atheletes.csv")):
    try:
        df = pd.read_csv(csv_path)
        return df
    except FileNotFoundError:
        print(f"❌ Error: CSV file not found at {csv_path}")
        return pd.DataFrame()

# KNN Model Training — now only using 'Age'
def train_knn_model(df):
    features = ['Age']
    knn = NearestNeighbors(n_neighbors=5)
    knn.fit(df[features])
    return knn

# Decision Tree Training — still using 'Age' to predict 'Sport'
def train_decision_tree(df):
    features = ['Age']
    X = df[features]
    y = df['Sport']
    dtree = DecisionTreeClassifier()
    dtree.fit(X, y)
    return dtree

# Weighted Scoring (optional, currently unused)
def weighted_score(row, weights):
    return sum(weights[feature] * row[feature] for feature in weights)

# Save trained models
def save_models(knn, dtree):
    with open(os.path.join(BASE_DIR, "knn_model.pkl"), "wb") as f:
        pickle.dump(knn, f)
    with open(os.path.join(BASE_DIR, "decision_tree_model.pkl"), "wb") as f:
        pickle.dump(dtree, f)

def get_top_matches(filters,
                    model_path=os.path.join(BASE_DIR, "knn_model.pkl"),
                    csv_path=os.path.join(BASE_DIR, "atheletes.csv")):

    df = load_data(csv_path)
    if df.empty:
        return []

    if filters.get("sport"):
        df = df[df["Sport"].str.lower() == filters["sport"].strip().lower()]
    if filters.get("age"):
        try:
            df = df[df["Age"] <= int(filters["age"])]
        except ValueError:
            pass
    if filters.get("gender"):
        df = df[df["Gender"].str.lower() == filters["gender"].strip().lower()]
    if filters.get("city"):
        df = df[df["City"].str.lower() == filters["city"].strip().lower()]
    if filters.get("state"):
        df = df[df["State"].str.lower() == filters["state"].strip().lower()]
    if filters.get("level"):
        df = df[df["Level"].str.lower() == filters["level"].strip().lower()]
    print("📥 Filter received:", filters)
    print("📊 Filtered results:")
    print(df.head(3))

    return df.head(10).to_dict(orient="records")

if __name__ == "_main_":
    df = load_data()
    knn = train_knn_model(df)
    dtree = train_decision_tree(df)
    save_models(knn, dtree)
    print("✅ Models trained and saved successfully.")
    print(df.head())        # See if data is loaded
