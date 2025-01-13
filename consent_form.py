
from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import get_db_connection

consent_bp = Blueprint('consent', __name__)

@consent_bp.route('/add-consent', methods=['GET', 'POST'])
def add_consent():
    conn = get_db_connection()
    if conn is None:
        flash("Database connection failed. Please try again later.", 'danger')
        return redirect(url_for('home'))

    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        child_id = request.form['child_id']
        vaccine_id = request.form['vaccine_id']
        date_given = request.form['date_given']
        consent_checkbox = request.form.get('consent_checkbox')  # Get the checkbox value

        if not consent_checkbox:
            flash("You must agree to the consent terms to proceed.", 'danger')
            return redirect(url_for('consent.show_consent_form'))

        try:
            cursor.execute(
                "INSERT INTO Consent (ChildID, VaccineID, DateGiven, Sign) VALUES (%s, %s, %s, %s)",
                (child_id, vaccine_id, date_given, 1)  # Sign will always be 1 because of checkbox
            )
            conn.commit()
            flash('Consent recorded successfully!', 'success')
        except Exception as e:
            flash(f'An error occurred: {e}', 'danger')
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('vaccination_history.view_vaccination_history'))

    return redirect(url_for('consent.show_consent_form'))

@consent_bp.route('/consent-form', methods=['GET'])
def show_consent_form():
    conn = get_db_connection()
    if conn is None:
        flash("Database connection failed. Please try again later.", 'danger')
        return redirect(url_for('home'))

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT ChildID, ChildName FROM Child")
        children = cursor.fetchall()
        cursor.execute("SELECT VaccineID, VaccineName FROM Vaccine")
        vaccines = cursor.fetchall()
    except Exception as e:
        flash(f'An error occurred while fetching data: {e}', 'danger')
        children, vaccines = [], []
    finally:
        cursor.close()
        conn.close()

    return render_template('consent_form.html', children=children, vaccines=vaccines)

