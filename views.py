from flask import render_template, request, redirect, url_for
from app import app,db
import math 

@app.route("/", methods=['GET', 'POST'])
def index():
  return render_template("index.html", page="Index")

@app.route("/result",  methods=['GET', 'POST'])
def result():
  if request.method == "POST":
        details = request.form
        name = details['name']
        tinggiBadan = details['bb']
        beratBadan = details['tb']
        #gender = details['gender']

        bmi = round(int(tinggiBadan) /((int(beratBadan)/100) ** 2), 1)

        if bmi < 18.5:
          status = 'Kurus'
        elif bmi < 22.9:
          status = 'Normal'
        elif bmi < 29.9:
          status = 'Gemuk'
        else:
          status = 'Obesitas'

        conn = db.connection
        cur = conn.cursor()
        cur.execute("INSERT INTO tb_bmi(name, tinggi_badan, berat_badan, bmi, status) VALUES (%s, %s, %s, %s, %s)", 
                    (name, beratBadan, tinggiBadan, bmi, status))
        conn.commit()
        #cur.close()
        resp = {'name' : name, 'bmi':bmi, 'status':status}
        print("BMI : ", bmi)
        return render_template("result.html", page="Result", resp=resp)
  return render_template("result.html", page="Result", resp=resp)

@app.route("/about")
def about():
  return render_template("about.html", page="About")

@app.route("/data", methods=['GET', 'POST'])
def data():
  conn = db.connection
  cur = conn.cursor()
  name =  request.args.get('name')
  print(name)
  if name != None:
    cur.execute("SElECT * FROM tb_bmi where name like  '%" + str(name) + "%'") 
  else:
    cur.execute("SElECT * FROM tb_bmi")
  container = []
  for id, name, tinggi_badan, berat_badan, bmi, status in cur.fetchall():
    container.append((id, name, tinggi_badan, berat_badan, bmi, status))
  return render_template("data.html", page="Result", resp=container)

@app.route("/hapus/<id>", methods=['GET', 'POST'])
def hapus(id):
  conn = db.connection
  cur = conn.cursor()
  cur.execute("DELETE FROM tb_bmi where id=%s", (id,))
  conn.commit()
  return redirect(url_for('data'))

@app.route("/update/<id>", methods=['GET', 'POST'])
def update(id):
  conn = db.connection
  cur = conn.cursor()
  if request.method == 'GET':
    cur.execute("SELECT * FROM tb_bmi where id=%s", (id,))
    container = []
    for id, name, tinggi_badan, berat_badan, bmi, status in cur.fetchall():
      container.append((id, name, tinggi_badan, berat_badan, bmi, status))
    return render_template('update.html', page="Update", resp=container)
  elif request.method == 'POST':
    details = request.form
    name = details['name']
    tinggiBadan = details['tb']
    beratBadan = details['bb']
    #gender = details['gender']

    bmi = round(float(tinggiBadan) /((float(beratBadan)/100) ** 2), 1)

    if bmi < 18.5:
      status = 'Kurus'
    elif bmi < 22.9:
      status = 'Normal'
    elif bmi < 29.9:
      status = 'Gemuk'
    else:
      status = 'Obesitas'
    cur.execute("UPDATE tb_bmi SET name=%s, tinggi_badan=%s, berat_badan=%s, bmi=%s, status=%s where id=%s", 
            (name, tinggiBadan, beratBadan, bmi, status, id))
    conn.commit()
    return redirect(url_for('data'))
  return render_template('update.html')

@app.route("/edit", strict_slashes=False)
@app.route("/edit/<int:id>", strict_slashes=False)
def edit(id=None):
  return render_template('update.html', name=id)
  


