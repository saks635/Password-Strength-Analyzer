from flask import Flask, render_template, request
from datetime import datetime
import csv, os, re

app = Flask(__name__)
LOG_FILE = 'password_logs.csv'

def check_password_strength(password):
    length_error = len(password) < 8
    digit_error = re.search(r"\d", password) is None
    uppercase_error = re.search(r"[A-Z]", password) is None
    lowercase_error = re.search(r"[a-z]", password) is None
    symbol_error = re.search(r"[!@#$%^&*(),.?\":{}|<>]", password) is None

    errors = [length_error, digit_error, uppercase_error, lowercase_error, symbol_error]
    strength = 5 - sum(errors)

    if strength <= 2:
        return "Weak"
    elif strength == 3 or strength == 4:
        return "Moderate"
    else:
        return "Strong"

def log_to_csv(password, strength):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['timestamp', 'password', 'strength'])
        writer.writerow([now, password, strength])

@app.route('/', methods=['GET', 'POST'])
def index():
    strength = ""
    if request.method == 'POST':
        password = request.form['password']
        strength = check_password_strength(password)
        log_to_csv(password, strength)
    return render_template('index.html', strength=strength)

if __name__ == '__main__':
    app.run(debug=True)
