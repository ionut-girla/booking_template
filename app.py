import datetime
import time

from functools import wraps
from flask import Flask
from flask import render_template
from flask import request
from flask import flash, redirect, url_for, get_flashed_messages, session
import mysql.connector
import os


if os.path.isfile('.env'):
    from dotenv import load_dotenv
    load_dotenv()

app = Flask(__name__, template_folder='templates', static_folder="static")
app.secret_key = 'dummysecrettrilathienkey'

def login_required(func):
   @wraps(func)
   def wrapper(*args, **kwargs):
       if 'logged_in' not in session:
           return redirect(url_for('render_sign_in'))
       elif 'logged_in' in session and session['logged_in'] == False:
           return redirect(url_for('render_sign_in'))
       return func(*args, **kwargs)
   return wrapper


@app.route('/')
def render_index():
    get_flashed_messages()
    return render_template('cover.html')


@app.route('/sign-in', methods=['GET'])
def render_sign_in():
    get_flashed_messages()
    return render_template('index.html')


@app.route('/register_new_user', methods=['GET'])
def render_register():
    get_flashed_messages()
    return render_template('register_user.html')


@app.route('/reservations_view', methods=['GET'])
@login_required
def render_reservations_view():
    get_flashed_messages()
    # Connect to the database
    conn = mysql.connector.connect(host=os.environ.get('DATABASE_HOST'),
                                   database=os.environ.get('DATABASE_NAME'),
                                   user=os.environ.get('DATABASE_USER'),
                                   password=os.environ.get('DATABASE_PASSWORD'))
    cur = conn.cursor()
    # Execute a SELECT query to retrieve the user's record
    # query = "SELECT tblfactura.seria, tblfactura.tipPlata, tblclienti.nume, tblclienti.prenume,tblcamera.descriere, " \
    #         "tblrezervarecamera.nrAdulti, tblrezervarecamera.nrCopii, tblrezervare.dataCheckin, " \
    #         "tblrezervare.dataCheckout, tblrezervare.codClient, tblrezervare.idRezervare, " \
    #         "tblrezervarecamera.codRezervare, tblcamera.idCamera, tblrezervarecamera.codCamera FROM tblfactura, " \
    #         "tblrezervare , tblcamera , tblrezervarecamera , tblclienti WHERE " \
    #         "tblrezervare.idRezervare=tblrezervarecamera.codRezervare AND " \
    #         "tblrezervarecamera.codCamera=tblcamera.idCamera AND tblrezervare.codClient=tblclienti.idClient AND " \
    #         "tblfactura.codRezervare=tblrezervare.idRezervare; "
    query = "SELECT tblfactura.seria, tblfactura.tipPlata, tblclienti.nume, tblclienti.prenume,tblcamera.descriere, tblrezervarecamera.nrAdulti, tblrezervarecamera.nrCopii, tblrezervare.dataCheckin, tblrezervare.dataCheckout, tblrezervare.codClient, tblrezervare.idRezervare, tblrezervarecamera.codRezervare, tblcamera.idCamera, tblrezervarecamera.codCamera FROM tblfactura, tblrezervare , tblcamera , tblrezervarecamera , tblclienti WHERE tblrezervare.idRezervare=tblrezervarecamera.codRezervare AND tblrezervarecamera.codCamera=tblcamera.idCamera AND tblrezervare.codClient=tblclienti.idClient AND tblfactura.codRezervare=tblrezervare.idRezervare;"

    cur.execute(query)
    results = cur.fetchall()

    # Close the cursor and connection
    cur.close()
    conn.close()
    current_date = datetime.datetime.now().date()
    # Convert the results to a list of dictionaries
    # results_dict = [{'serie_factura': row[0],
    #                  'tip_plata': row[1],
    #                  'nume': row[2],
    #                  'prenume': row[3],
    #                  'descriere_camera': row[4],
    #                  'adulti': row[5],
    #                  'copii': row[6],
    #                  'data_start': row[7],
    #                  'data_stop': row[8]
    #                  }
    #                 for row in results if row[7] > current_date]

    results_dict = [{'serie_factura': row[0],
                     'tip_plata': row[1],
                     'nume': row[2],
                     'prenume': row[3],
                     'descriere_camera': row[4],
                     'adulti': row[5],
                     'copii': row[6],
                     'data_start': row[7],
                     'data_stop': row[8]
                     }
                    for row in results]
    # Render the template
    return render_template('reservations_view.html', results=results_dict)


@app.route('/success', methods=['GET'])
def render_success():
    get_flashed_messages()
    return render_template('success.html')


@app.route('/register_new_user', methods=['POST'])
def register_new_user():
    print('in register_new_user')
    name = request.form['name']
    first_name = request.form['first_name']
    cnp = request.form['cnp']
    phone = request.form['phone']
    judet = request.form['judet']
    localitate = request.form['localitate']
    # Check if the username and password are correct

    # Connect to the database
    conn = mysql.connector.connect(host=os.environ.get('DATABASE_HOST'),
                                   database=os.environ.get('DATABASE_NAME'),
                                   user=os.environ.get('DATABASE_USER'),
                                   password=os.environ.get('DATABASE_PASSWORD'))
    cur = conn.cursor()
    # Execute a SELECT query to retrieve the user's record
    query = "INSERT INTO tblclienti (nume, prenume, cnp, nrTelefon, judet, localitate) VALUES (%s, %s, %s, %s, %s, %s)"
    cur.execute(query, (name, first_name, cnp, phone, judet, localitate))
    conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()
    session['logged_in'] = False
    session['user'] = (name, first_name, cnp, phone, judet, localitate)

    return render_template('cover.html', session=session)


@app.route('/sign-out')
def sign_out():
    session['logged_in'] = False
    session['user'] = ''
    return render_template('cover.html')

@app.route('/sign-in', methods=['POST'])
def sign_in():
    nr_telefon = request.form['floatingInput']
    cnp = request.form['floatingPassword']
    # Check if the username and password are correct

    # Connect to the database
    conn = mysql.connector.connect(host=os.environ.get('DATABASE_HOST'),
                                   database=os.environ.get('DATABASE_NAME'),
                                   user=os.environ.get('DATABASE_USER'),
                                   password=os.environ.get('DATABASE_PASSWORD'))
    cur = conn.cursor()
    # 0756268349
    # 1881118250604
    # Execute a SELECT query to retrieve the user's record
    query = "SELECT * FROM tblclienti WHERE nrTelefon = %s AND cnp = %s"
    cur.execute(query, (nr_telefon, cnp))
    user = cur.fetchone()

    # Close the cursor and connection
    cur.close()
    conn.close()

    if user is not None:
        # The username and password are correct
        session['logged_in'] = True
        session['user'] = user
        return render_template('cover.html', session=session)
    else:
        # The username and password are incorrect
        flash('Invalid username or password.')
        return redirect(url_for('render_sign_in'))


@app.route('/cover', methods=['GET'])
def render_cover():
    print('in cover sign in')
    return render_template('cover.html')


def get_entries():
    # Connect to the database
    conn = mysql.connector.connect(host=os.environ.get('DATABASE_HOST'),
                                   database=os.environ.get('DATABASE_NAME'),
                                   user=os.environ.get('DATABASE_USER'),
                                   password=os.environ.get('DATABASE_PASSWORD'))
    cur = conn.cursor()

    # Execute a SELECT query to retrieve the user's record

    query = "SELECT * FROM tblcamera"
    cur.execute(query)
    entries = cur.fetchall()

    # Close the cursor and connection
    cur.close()
    conn.close()

    return entries


@app.route('/entries')
@login_required
def show_entries():
    entries = get_entries()
    return render_template('entries.html', entries=entries)


@app.route('/rezervare', methods=['POST'])
@login_required
def reserve_room():
    # Perform the desired action
    ...
    entry_id = request.form['entry_id']
    entry_price = request.form['entry_price']
    entry_description = request.form['entry_description']
    entries = [[entry_id, entry_price, entry_description]]
    print(f'entry_id ={entry_id} while entry_price ={entry_price}')
    return render_template('rezervare.html', entries=entries, session=session)


@app.route('/save_reservation', methods=['POST'])
@login_required
def save_reservation():
    # Perform the desired action
    ...
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    if request.form['adults'] == '':
        adults = 1
    else:
        adults = request.form['adults']
    if request.form['children'] == '':
        children = 0
    else:
        children = request.form['children']
    room_code = request.form['room_code']

    if 'client_code' in request.form:
        client_code = request.form['client_code']
    else:
        client_code = session['user'][0]
    print(f'entry_id ={start_date} while entry_price ={end_date}, client_code= {client_code}')
    number_of_days = datetime.datetime(int(end_date.split('-')[0]), int(end_date.split('-')[1]), int(end_date.split('-')[2])) - \
                     datetime.datetime(int(start_date.split('-')[0]), int(start_date.split('-')[1]), int(start_date.split('-')[2]))
    number_of_days = number_of_days.days


    # Connect to the database
    conn = mysql.connector.connect(host=os.environ.get('DATABASE_HOST'),
                                   database=os.environ.get('DATABASE_NAME'),
                                   user=os.environ.get('DATABASE_USER'),
                                   password=os.environ.get('DATABASE_PASSWORD'))
    cur = conn.cursor()
    # Execute a SELECT query to retrieve the user's record
    query = "INSERT INTO tblrezervare (codClient, dataCheckin, dataCheckout, nrZile) VALUES (%s, %s, %s, %s)"
    values = (client_code, start_date, end_date, number_of_days)
    cur.execute(query, values)
    conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()


    # Connect to the database
    conn = mysql.connector.connect(host=os.environ.get('DATABASE_HOST'),
                                   database=os.environ.get('DATABASE_NAME'),
                                   user=os.environ.get('DATABASE_USER'),
                                   password=os.environ.get('DATABASE_PASSWORD'))
    cur = conn.cursor()
    # 0756268349
    # 1881118250604
    # Execute a SELECT query to retrieve the user's record
    query = "SELECT idRezervare FROM tblrezervare WHERE codClient = %s AND dataCheckin = %s AND dataCheckout = %s AND nrZile = %s"

    values = (client_code, start_date, end_date, number_of_days)
    cur.execute(query, values)
    id_rezervare = cur.fetchone()
    id_rezervare = id_rezervare[0]
    # Close the cursor and connection
    cur.close()
    conn.close()


    # Connect to the database
    conn = mysql.connector.connect(host=os.environ.get('DATABASE_HOST'),
                                   database=os.environ.get('DATABASE_NAME'),
                                   user=os.environ.get('DATABASE_USER'),
                                   password=os.environ.get('DATABASE_PASSWORD'))
    cur = conn.cursor()
    # Execute a SELECT query to retrieve the user's record
    query = "INSERT INTO tblrezervarecamera (codCamera, codRezervare, nrAdulti, nrCopii) VALUES (%s, %s, %s, %s)"
    values = (room_code, id_rezervare, adults, children)
    cur.execute(query, values)
    conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()

    return render_template('success.html')

if __name__ == '__main__':
    app.run()
