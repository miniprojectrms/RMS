import os
import random

from database import *
from flask import Flask, jsonify, render_template, request, session
from flask_mail import Mail, Message

from data import entry

#from analysis import bargraph, analysis

secretkey = os.urandom(24)
app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'miniprojectrms061@gmail.com'
app.config['MAIL_PASSWORD'] = "lvllzuckbrprfnxu"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
app.secret_key = secretkey


@app.route('/')  #URL Pattern
def home():
  return render_template('index.html')


@app.route('/index2')
def home1():
  roll = session['roll']
  return render_template('index2.html', roll=roll)


@app.route('/kritunga')
def kritunga():
  name = "kritunga"
  return render_template('kritunga.html', name=name)


@app.route('/search', methods=['POST'])
def shift():
  name = request.form.get('searchInput')
  session['name'] = name
  return render_template('kritunga.html', name=name)


@app.route('/reserve')
def reserve():
  roll = session['roll']
  return render_template('reservation.html', roll=roll)


def generate_otp():
  return str(random.randint(100000, 999999))


@app.route('/send-otp', methods=['GET', 'POST'])
def check_rollno():
  gmail = str(request.form.get('mail'))
  session['mail'] = gmail
  #session['roll'] = roll
  #gmail = gmail.lower() + '@gcet.edu.in'
  #print(gmail)
  session['otp1'] = generate_otp()
  #print(session['otp1'])
  msg = Message(
      "OTP to view Your result",
      sender="miniprojectrms061@gmail.com",
      recipients=[gmail],
  )
  msg.body = f"Your OTP:{session['otp1']}"
  mail.send(msg)
  return render_template("index1.html")


@app.route('/check-otp', methods=["POST", "GET"])
def check_otp():
  roll = str(request.form.get('name'))
  session['roll'] = roll
  otp2 = str(request.form.get('otp'))
  if session['otp1'] == otp2:
    return render_template("index2.html", roll=roll)
  return render_template("index1.html", k="Invalid OTP")


@app.route('/dbentry', methods=["POST"])
def dbentry():
  name = str(request.form.get('name'))
  email = str(request.form.get('email'))
  date = request.form.get('date')
  time = request.form.get('time')
  people = request.form.get('people')
  entry(name, email, date, time, people)
  session['name1'] = name
  session['time'] = time
  session['date'] = date
  session['people'] = people
  msg = Message(
      "Confirmed your Table",
      sender="miniprojectrms061@gmail.com",
      recipients=[email],
  )
  msg.body = f"Thank You  {session['name1']}  You Have Reserved A Table At Time : {session['time']} Date :{session['date']} No of people :{session['people']} Your Alloted Waiter is Krishna "
  mail.send(msg)
  roll = session['roll']
  return render_template("reservation1.html", roll=roll)


@app.route('/receive_data', methods=['POST'])
def receive_data():
  data = request.get_json()
  item = []
  for i in data:
    item.append(i['name'])
  print(item)
  email = session['mail']
  msg = Message(
      "Your Orders",
      sender="miniprojectrms061@gmail.com",
      recipients=[email],
  )
  name = session['roll']
  msg.body = f" Thank you {name} . Your ordered items are :{item}"
  mail.send(msg)

  response = {"message": "Data received successfully"}
  return jsonify(response)


if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')
