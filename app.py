from flask import Flask, render_template, request, session, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "Prediksi2023"
app.secret_key = "geyygafljwrnvdskdcnlkbdbdj"

userpass = "mysql+pymysql://root:@"
basedir = "127.0.0.1"
dbname = "/prediksiemas"

app.config["SQLALCHEMY_DATABASE_URI"] = userpass + basedir + dbname
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Hasil(db.Model):
    no = db.Column(db.Integer, primary_key=True)
    tanggal = db.Column(db.String(50), nullable=False)
    prediksi = db.Column(db.String(100), nullable=False)

    def __init__(self, no, tanggal, prediksi):
        self.no = no
        self.tanggal = tanggal
        self.prediksi = prediksi

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def log():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if username == 'razanan' and password == 'predict11':
            session['username'] = username
            return redirect(url_for('admin'))
        
        else:
            return redirect(url_for('log'))
        
    return render_template("login.html")

@app.route("/prediksi")
def prediksi():
    data_prediksi = db.session.query(Hasil)
    return render_template("prediksi.html", data = data_prediksi)

@app.route("/admin")
def admin():
    data_prediksi = db.session.query(Hasil)
    return render_template("admin.html", data = data_prediksi)

@app.route("/input", methods=['GET', 'POST'])
def input():
    if request.method == 'POST':
        no = request.form['no']
        tanggal = request.form['tanggal']
        prediksi = request.form['prediksi']

        add_data = Hasil(no, tanggal, prediksi)

        db.session.add(add_data)
        db.session.commit()

        return redirect(url_for('admin'))
    return render_template("input.html")

@app.route('/delete/<int:no>')
def delete(no):
    data_hasil = Hasil.query.get(no)
    db.session.delete(data_hasil)
    db.session.commit()

    return redirect(url_for('admin'))

if __name__ == "__main__":
    app.run(debug=True)