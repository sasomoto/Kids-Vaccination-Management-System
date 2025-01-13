from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import get_db_connection

add_vaccination_bp = Blueprint('add_vaccination', __name__)

@add_vaccination_bp.route('/add-vaccination', methods=['GET', 'POST'])
def add_vaccination():
    if request.method == 'POST':
        child_id = request.form['child_id']
        vaccine_id = request.form['vaccine_id']
        vaccination_date = request.form['vaccination_date']
        lot_number = request.form['lot_number']
        provider = request.form['provider']

        conn = get_db_connection()
        if conn is None:
            flash("Database connection failed. Please try again later.", 'danger')
            return redirect(url_for('home'))

        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO VaccinationHistory (ChildID, VaccineID, FirstDate, LotNumber, Provider) VALUES (%s, %s, %s, %s, %s)",
                (child_id, vaccine_id, vaccination_date, lot_number, provider)
            )
            conn.commit()
            flash('Vaccination record added successfully!', 'success')
        except Exception as e:
            flash(f'An error occurred: {e}', 'danger')
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('vaccination_history.view_vaccination_history'))

    conn = get_db_connection()
    if conn is None:
        flash("Database connection failed. Please try again later.", 'danger')
        return redirect(url_for('home'))

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT VaccineID, VaccineName FROM Vaccine")
    vaccines = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('add_vaccination.html', vaccines=vaccines)








