from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import get_db_connection  # Import from db.py

add_child_bp = Blueprint('add_child', __name__)

@add_child_bp.route('/add-child', methods=['GET', 'POST'])
def add_child():
    conn = get_db_connection()
    if conn is None:
        flash("Database connection failed. Please try again later.", 'danger')
        return redirect(url_for('home'))

    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        name = request.form['name']
        dob = request.form['dob']
        guardian_id = request.form['guardian_id']
        gender = request.form['gender']
        allergies = request.form.get('allergies', '')

        try:
            cursor.execute(
                "INSERT INTO Child (ChildName, ChildDOB, GuardianID, ChildGender, Allergies) VALUES (%s, %s, %s, %s, %s)",
                (name, dob, guardian_id, gender, allergies)
            )
            conn.commit()
            flash('Child added successfully!', 'success')
        except Exception as e:
            flash(f'An error occurred: {e}', 'danger')
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('children.view_children'))

    cursor.execute("SELECT GuardianID, GuardianName FROM Guardian")
    guardians = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('add_child.html', guardians=guardians)
