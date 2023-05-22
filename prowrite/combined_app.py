from flask import Flask, request, redirect, render_template
import ibm_db
from flask import flash
from gingerit.gingerit import GingerIt
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

import nltk

app = Flask(__name__)

nltk.download('punkt')

# Configure the IBM DB2 database connection
conn =  ibm_db.connect("database=bludb;hostname=b1bc1829-6f45-4cd4-bef4-10cf081900bf.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud; port=32304; uid = jsg48928;password = 0W6iLqdmqtUCiLlq;security =SSL;sslcertificate = DigiCertGlobalRootCA.crt ","","")
# Create a user table in the database
# stmt = ibm_db.exec_immediate(conn, "CREATE TABLE users (id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY, email VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL)")

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup_form.html')

    email = request.form['email']
    password = request.form['password']

    # Prepare the SQL statement with parameter markers
    stmt = ibm_db.prepare(conn, "INSERT INTO users (email, password) VALUES (?, ?)")

    # Bind the parameter values to the SQL statement
    ibm_db.bind_param(stmt, 1, email)
    ibm_db.bind_param(stmt, 2, password)

    # Execute the SQL statement
    ibm_db.execute(stmt)

    return redirect('/')

# Login route
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login_form.html")

    email = request.form['email']
    password = request.form['password']

    # Check if the user exists in the database
    stmt = ibm_db.prepare(conn, "SELECT * FROM users WHERE email = ? AND password = ?")
    ibm_db.bind_param(stmt, 1, email)
    ibm_db.bind_param(stmt, 2, password)
    ibm_db.execute(stmt)
    result = ibm_db.fetch_assoc(stmt)

    if result:
        a = f"Welcome back, {''.join(email.split('@gmail.com'))}!"
        print(a)
        return render_template('home.html', mail=a)
    else:
        return "Invalid email or password"

# Home route
@app.route('/home')
def home():
    return render_template("home.html")

#about
@app.route('/about')
def about():
    return render_template('about.html')

# Grammar correction route
@app.route('/grammar_home')
def grammar_home():
    return render_template('grammar.html')

@app.route('/grammar', methods=['POST'])
def correct_grammar():
    text = request.form['text']
    corrected_text = GingerIt().parse(text)
    result = corrected_text['result']
    return render_template('grammar.html', result=result)

# Spell correction route
@app.route("/sent_correct", methods=["GET", "POST"])
def spell_correct():
    if request.method == "GET":
        return render_template("spell.html")
    else:
        if not request.form["SENT"]:
            return redirect("/sent_correct")

        text = request.form["SENT"]
        parser = GingerIt()
        result = parser.parse(text)['result']
        return render_template('spell.html', output1=result)

# Text summarization route
@app.route('/summarize', methods=['GET', 'POST'])
def summarize():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        paragraph = request.form['paragraph']
        parser = PlaintextParser.from_string(paragraph, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, 10)  # Summarize into 10 sentences
        return render_template('summary.html', summary=summary)

if __name__ == '__main__':
    app.run("0.0.0.0",debug=True)