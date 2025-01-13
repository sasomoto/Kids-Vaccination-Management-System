from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import get_db_connection  # Import from db.py

add_vaccine_bp = Blueprint('add_vaccine', __name__)

@add_vaccine_bp.route('/add-vaccine', methods=['GET', 'POST'])
def add_vaccine():
    if request.method == 'POST':
        vaccine_name = request.form['vaccine_name']
        recommended_age_range = request.form['recommended_age_range']
        exclusions = request.form['exclusions']
        v_cost = request.form['v_cost']
        hospital_id = request.form['hospital_id']

        conn = get_db_connection()
        if conn is None:
            flash("Database connection failed. Please try again later.", 'danger')
            return redirect(url_for('home'))

        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO Vaccine (VaccineName, RecommendedAgeRange, Exclusions, V_Cost, HospitalID) VALUES (%s, %s, %s, %s, %s)",
                (vaccine_name, recommended_age_range, exclusions, v_cost, hospital_id)
            )
            conn.commit()
            flash('Vaccine added successfully!', 'success')
        except Exception as e:
            flash(f'An error occurred: {e}', 'danger')
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('vaccines.view_vaccines'))

    # Fetch hospitals to populate the dropdown
    conn = get_db_connection()
    if conn is None:
        flash("Database connection failed. Please try again later.", 'danger')
        return redirect(url_for('home'))

    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT HospitalID, H_Name FROM Hospital")
        hospitals = cursor.fetchall()
    except Exception as e:
        flash(f'An error occurred while fetching hospitals: {e}', 'danger')
        hospitals = []
    finally:
        cursor.close()
        conn.close()

    return render_template('add_vaccine.html', hospitals=hospitals)


