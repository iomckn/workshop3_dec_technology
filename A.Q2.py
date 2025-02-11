from flask import Flask, request, jsonify
import pickle
import numpy as np
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
        predictions = []

        # Obtenir la prédiction de chaque modèle
        for model_name, model in loaded_models.items():
            pred = int(model.predict(features)[0])  # Conversion en int pour JSON
            predictions.append(pred)
        
        # Appliquer le vote majoritaire
        consensus_prediction = int(Counter(predictions).most_common(1)[0][0])  # Conversion en int
        predicted_class = iris.target_names[consensus_prediction]
        
        response = {
            "input": {
                "sepal_length": sepal_length,
                "sepal_width": sepal_width,
                "petal_length": petal_length,
                "petal_width": petal_width
            },
            "predictions": predictions,
            "consensus_prediction": predicted_class
        }
        
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
