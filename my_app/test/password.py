from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

@app.route('/<password>')
def index(password):
    hashed_value = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
    #result = check_password_hash(hashed_value, password)
    return hashed_value

if __name__ == '__main__':
    app.run(debug=True)
