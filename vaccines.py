from flask import Blueprint, render_template
from db import get_db_connection  # Import from db.py

vaccines_bp = Blueprint('vaccines', __name__)

@vaccines_bp.route('/vaccines', methods=['GET'])
def view_vaccines():
    conn = get_db_connection()
    if conn is None:
        return "Database connection failed.", 500

    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT VaccineID, VaccineName, RecommendedAgeRange, Exclusions, V_Cost, HospitalID FROM Vaccine")
    vaccines = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('vaccines.html', vaccines=vaccines)

