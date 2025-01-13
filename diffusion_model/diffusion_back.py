import torch
from flask import Flask, request, jsonify
from torch import Tensor

from flask_cors import CORS

app = Flask(__name__)
# Activer CORS pour toutes les routes
CORS(app)




# Charger le modèle complet
# Charger le modèle scripté
def load_model(path):
    model = torch.jit.load(path)  # Charger un modèle scripté
    model.eval()  # Passer le modèle en mode évaluation
    return model

# Chemin vers votre modèle sauvegardé
MODEL_PATH = "trained_model.pt"
model = load_model(MODEL_PATH)

# Route pour prédire
@app.route('/predict', methods=['POST'])

def predict():
    try:
        # Récupérer les données JSON envoyées
        input_data = request.get_json()

        # Valider les données reçues
        if 'features' not in input_data:
            return jsonify({'error': 'Les données doivent contenir une clé "features".'}), 400

        # Obtenir les caractéristiques (features) et les mettre au bon format
        features = input_data['features']  # Doit être une liste ou un tableau
        features = Tensor([features])  # Convertir en tenseur PyTorch
        
        # Appliquer le scaler sur les caractéristiques avant de faire la prédiction
        

        # Faire une prédiction
        with torch.no_grad():
            prediction = model(features).numpy()

        # Formatage de la prédiction
        yhat = prediction[0][0]  # Extraire la prédiction (en supposant que c'est un tableau 2D)
        print(yhat)
        print(prediction)

        formatted_prediction = {
            'predicted_value': "%.3f" % yhat,  # Formater la valeur de la prédiction
            'predicted_class': int(round(yhat))  # Classifier la prédiction comme 0 ou 1
        }

        # Afficher la prédiction dans le format que vous souhaitez
        print('Predicted: %.3f (class=%d)' % (yhat, round(yhat)))

        # Retourner la prédiction formatée dans la réponse JSON
        return jsonify(formatted_prediction)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':

    app.run(host="0.0.0.0", port=5000, debug=True)