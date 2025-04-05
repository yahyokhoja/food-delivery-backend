from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)

# Строка подключения для PostgreSQL (без SSL)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://<username>:<password>@<host>:<port>/<database>'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализация SQLAlchemy
db = SQLAlchemy(app)
CORS(app)  # Разрешаем CORS для фронтенда

# Модель пользователя
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=True)

# Создание всех таблиц в БД
with app.app_context():
    db.create_all()

# API для регистрации пользователей
@app.route('/api/register', methods=['POST'])
def register_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    phone = data.get('phone')

    # Проверка обязательных полей
    if not name or not email or not password:
        return jsonify({'message': 'Имя, email и пароль обязательны'}), 400

    # Проверка на существование пользователя с таким email
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'message': 'Пользователь с таким email уже существует'}), 409

    # Создание нового пользователя
    new_user = User(name=name, email=email, password=password, phone=phone)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Пользователь зарегистрирован', 'user_id': new_user.id})

# Запуск сервера
if __name__ == '__main__':
    app.run(debug=True)
