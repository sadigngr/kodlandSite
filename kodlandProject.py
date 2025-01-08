import sqlite3
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

db_file = 'quiz.db'

with sqlite3.connect(db_file) as conn:
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS QuizResponse (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            question1 TEXT NOT NULL,
            question2 TEXT NOT NULL,
            question3 TEXT NOT NULL,
            question4 TEXT NOT NULL,
            question5 TEXT NOT NULL,
            score INTEGER
        )
    ''')
    conn.commit()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Yapay Zeka Quiz'i'</title>
    <style>
        body {
            position: relative;
            min-height: 100vh;
        }

        footer {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            text-align: center;
        }
    </style>
</head>
<body>
    <h1>Yapay Zeka Quiz'i'</h1>
    <form method="POST">
        <h2>Isminiz Nedir?</h2>
        <input type="text" name="username" required>

        <h2>Soru 1: Asagidaki kutuphanelerden hangisi python'da yapay zeka gelistirme icin yaygin olarak kullanilir'?</h2>
        <input type="radio" name="question1" value="django" required> Django<br>
        <input type="radio" name="question1" value="tensorflow"> TensorFlow<br>
        <input type="radio" name="question1" value="flask"> Flask<br>

        <h2>Soru 2: "AI" kelimesinin acilimi nedir?</h2>
        <input type="radio" name="question2" value="Artificial Intelligence" required> Artificial Intelligence<br>
        <input type="radio" name="question2" value="Automated Interaction"> Automated Interaction<br>
        <input type="radio" name="question2" value="Advanced Integration"> Advanced Integration<br>

        <h2>Soru 3: Yapay zeka ile ust seviye program gelistirmede hangi programlama dili daha cok kullanilir?</h2>
        <input type="radio" name="question3" value="C++" required> C++<br>
        <input type="radio" name="question3" value="Python"> Python<br>
        <input type="radio" name="question3" value="HTML"> HTML<br>

        <h2>Soru 4: Yapay zekanin hangi dali, robotlar,n cevrelerini algilamasini saglamak icin kullanilir?</h2>
        <input type="radio" name="question4" value="Computer Vision" required> Computer Vision<br>
        <input type="radio" name="question4" value="Natural Language Processing"> Natural Language Processing<br>
        <input type="radio" name="question4" value="Reinforcement Learning"> Reinforcement Learning<br>

        <h2>Soru 5: Yapay zeka hangi amacla genellikle "Derin Ogrenme" kullanilarak egitilir?</h2>
        <input type="radio" name="question5" value="Simulation" required> Simulation<br>
        <input type="radio" name="question5" value="Data Compression"> Data Compression<br>
        <input type="radio" name="question5" value="Pattern Recognition"> Pattern Recognition<br>

        <br>
        <input type="submit" value="Testi Bitir">
        <br>
        <br>
        <br>
        <br>
        <br>
        <br>

        <div style="position: absolute; top: 10px; right: 10px;">
            <p>Best Score: {{ best_score }}</p>
        </div>
    </form>
    <footer>
        Basarilar!<br> 
                Puanlama, dogru cevaplar +1, yanlis cevaplar -1 puan olmak uzere yapilir.<br>
                Puaniniz 0'dan dusuk olamaz.<br>

                Sadi Gungor
    </footer>
</body>
</html>
"""

# Doğru cevaplar
def get_score(question1, question2, question3, question4, question5):
    score = 0

    score += (1 if question1 == "tensorflow" else -1) + (1 if question2 == "Artificial Intelligence" else -1) + (1 if question3 == "Python" else -1) + (1 if question4 == "Computer Vision" else -1) + (1 if question5 == "Pattern Recognition" else -1)

    if score < 0:
        score = 0
    
    return score

@app.route('/', methods=['GET', 'POST'])
def quiz():
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT MAX(score) FROM QuizResponse')
        best_score = cursor.fetchone()[0]
        if best_score is None:
            best_score = 0

    if request.method == 'POST':
        username = request.form.get('username')
        question1 = request.form.get('question1')
        question2 = request.form.get('question2')
        question3 = request.form.get('question3')
        question4 = request.form.get('question4')
        question5 = request.form.get('question5')

        score = get_score(question1, question2, question3, question4, question5)

        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO QuizResponse (username, question1, question2, question3, question4, question5, score)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (username, question1, question2, question3, question4, question5, score))
            conn.commit()

        return redirect(url_for('thank_you', username=username, score=score))

    return render_template_string(HTML_TEMPLATE, best_score=best_score)

@app.route('/thank-you')
def thank_you():
    username = request.args.get('username', 'Guest')
    score = request.args.get('score', '0')
    return f"<h1>Katildiginiz Icin Tesekkurler, {username}!</h1><h2>Skorunuz: {score}</h2>"

if __name__ == '__main__':
    app.run(debug=True)

