from flask import Blueprint, render_template, flash, redirect, url_for
from db import get_db_connection

vaccination_history_bp = Blueprint('vaccination_history', __name__)

@vaccination_history_bp.route('/vaccination-history', methods=['GET'])
def view_vaccination_history():
    conn = get_db_connection()
    if conn is None:
        flash("Database connection failed. Please try again later.", 'danger')
        return redirect(url_for('home'))

    cursor = conn.cursor(dictionary=True)

    # Fetching child ID, child name, and vaccination details
    cursor.execute("""
        SELECT vh.ChildID, c.ChildName, v.VaccineName, vh.FirstDate, vh.LotNumber, vh.Provider
        FROM VaccinationHistory vh
        JOIN Child c ON vh.ChildID = c.ChildID
        JOIN Vaccine v ON vh.VaccineID = v.VaccineID
    """)
    vaccination_history = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('vaccination_history.html', vaccination_history=vaccination_history)



