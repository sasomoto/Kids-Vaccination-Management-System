from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import get_db_connection  # Import from db.py

add_guardian_bp = Blueprint('add_guardian', __name__)

@add_guardian_bp.route('/add-guardian', methods=['GET', 'POST'])
def add_guardian():
    if request.method == 'POST':
        guardian_name = request.form['guardian_name']
        guardian_contact = request.form['guardian_contact']

        conn = get_db_connection()
        if conn is None:
            flash("Database connection failed. Please try again later.", 'danger')
            return redirect(url_for('home'))

        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO Guardian (GuardianName, GuardianContact) VALUES (%s, %s)",
                (guardian_name, guardian_contact)
            )
            conn.commit()
            flash('Guardian added successfully!', 'success')
        except Exception as e:
            flash(f'An error occurred: {e}', 'danger')
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('guardians.view_guardians'))

    return render_template('add_guardian.html')

