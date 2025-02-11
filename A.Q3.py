from flask import Flask, request, jsonify
import pickle
import numpy as np
import json
from collections import Counter
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

# Charger le dataset Iris
iris = datasets.load_iris()
X, y = iris.data, iris.target

# Séparer les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entraîner plusieurs modèles
models = {
    "logistic_regression": LogisticRegression(max_iter=200),
    "decision_tree": DecisionTreeClassifier(),
    "random_forest": RandomForestClassifier(n_estimators=100, random_state=42),
    "svm": SVC(probability=True)
}

for name, model in models.items():
    model.fit(X_train, y_train)
    with open(f"{name}.pkl", "wb") as f:
        pickle.dump(model, f)

# Charger les modèles
loaded_models = {}
for name in models.keys():
    with open(f"{name}.pkl", "rb") as f:
        loaded_models[name] = pickle.load(f)

# Initialiser ou charger les poids des modèles
weights_file = "model_weights.json"
try:
    with open(weights_file, "r") as f:
        model_weights = json.load(f)
except FileNotFoundError:
    model_weights = {name: 1.0 for name in models.keys()}
    with open(weights_file, "w") as f:
        json.dump(model_weights, f)

# Flask App
app = Flask(__name__)

@app.route('/')
def home():
    return "Iris Model API is running! Use /predict to get predictions."

@app.route('/predict', methods=['GET'])
def predict():
    try:
        sepal_length = float(request.args.get('sepal_length'))
        sepal_width = float(request.args.get('sepal_width'))
        petal_length = float(request.args.get('petal_length'))
        petal_width = float(request.args.get('petal_width'))
        
        features = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
        weighted_votes = {}
        predictions = []

        # Collecter les prédictions pondérées
        for model_name, model in loaded_models.items():
            pred = int(model.predict(features)[0])
            predictions.append(pred)
            weighted_votes[pred] = weighted_votes.get(pred, 0) + model_weights[model_name]
        
        # Déterminer la classe avec le score pondéré le plus élevé
        consensus_prediction = max(weighted_votes, key=weighted_votes.get)
        predicted_class = iris.target_names[consensus_prediction]
        
        response = {
            "input": {
                "sepal_length": sepal_length,
                "sepal_width": sepal_width,
                "petal_length": petal_length,
                "petal_width": petal_width
            },
            "predictions": predictions,
            "weights": model_weights,
            "consensus_prediction": predicted_class
        }
        
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/update_weights', methods=['POST'])
def update_weights():
    try:
        data = request.json
        correct_label = iris.target_names.index(data["correct_label"])
        
        for model_name, model in loaded_models.items():
            pred = int(model.predict([data["features"]])[0])
            if pred == correct_label:
                model_weights[model_name] += 0.1  # Récompense
            else:
                model_weights[model_name] = max(0.1, model_weights[model_name] - 0.1)  # Pénalité
        
        with open(weights_file, "w") as f:
            json.dump(model_weights, f)
        
        return jsonify({"message": "Weights updated successfully", "new_weights": model_weights})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
