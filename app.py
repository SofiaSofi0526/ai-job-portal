from flask import Flask, render_template, request, redirect
import csv

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    full_name = request.form.get('full_name', 'N/A')
    email = request.form.get('email', 'N/A')
    position = request.form.get('position', 'N/A')

    if full_name == 'N/A' or email == 'N/A' or position == 'N/A':
        return "Error: Missing form fields. Please ensure all fields are filled.", 400

    # Save data to CSV
    with open('applications.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([full_name, email, position])

    return render_template('success.html', full_name=full_name, email=email, position=position)

@app.route('/admin')
def admin():
    data = []
    with open('applications.csv', newline='') as file:
        reader = csv.reader(file)
        data = list(reader)
    return render_template('admin.html', data=data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        password = request.form['password']
        if password == 'admin123':
            return redirect('/admin')  # corrected here
        else:
            error = 'Invalid password. Please try again.'
    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)
