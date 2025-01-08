from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from models.user import User
from chatbot import qa_chain
from config import Config  # Assurez-vous que cette variable existe dans config.py pour la clé secrète

# Fonction pour générer le token JWT
def generate_token(user_id):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Le token expire dans 1 heure
    token = jwt.encode(
        {'user_id': user_id, 'exp': expiration_time},
        Config.SECRET_KEY,  # La clé secrète à utiliser pour encoder le token
        algorithm='HS256'
    )
    return token

def init_routes(app, mysql):
    # Route pour l'inscription
    @app.route('/register', methods=['POST'])
    def register():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'message': 'Username and password are required'}), 400

        # Vérifier si l'utilisateur existe déjà
        if User.get_by_username(mysql, username):
            return jsonify({'message': 'L\'utilisateur existe déjà.'}), 400

        # Hachage du mot de passe avant de le stocker
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Créer un nouvel utilisateur avec le mot de passe haché
        User.create(mysql, username, hashed_password)
        return jsonify({'message': 'Utilisateur créé avec succès !'}), 201

    # Route pour la connexion
    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'message': 'Username and password are required'}), 400

        user = User.get_by_username(mysql, username)
        if user:
            if check_password_hash(user[2], password):  # Assurez-vous que `user[2]` est bien le mot de passe haché
                # Générer un token JWT
                token = generate_token(user[0])  # L'ID de l'utilisateur est dans user[0]
                return jsonify({
                    'message': 'Connexion réussie!',
                    'token': token
                }), 200
            else:
                return jsonify({'message': 'Nom d\'utilisateur ou mot de passe incorrect.'}), 401
        else:
            return jsonify({'message': 'Nom d\'utilisateur ou mot de passe incorrect.'}), 401

    # Route pour poser une question au chatbot
    @app.route('/ask', methods=['POST'])
    def ask():
        user_input = request.json.get('question')

        if user_input:
            # Interroger la chaîne de récupération avec la question de l'utilisateur
            result = qa_chain.invoke({"query": user_input})

            # Convertir les documents source en chaînes de caractères
            source_documents = [str(doc) for doc in result['source_documents']]

            # Limiter la réponse pour éviter des longueurs excessives
            response_text = result['result'][:500]

            # Renvoi de la réponse
            return jsonify({
                'response': response_text,
                'sources': source_documents
            })
        return jsonify({'error': 'No question provided'}), 400
