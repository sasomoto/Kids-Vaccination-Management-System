from flask import Blueprint, render_template
from db import get_db_connection  # Import from db.py

guardians_bp = Blueprint('guardians', __name__)

@guardians_bp.route('/guardians', methods=['GET'])
def view_guardians():
    conn = get_db_connection()
    if conn is None:
        return "Database connection failed.", 500

    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT GuardianID, GuardianName, GuardianContact FROM Guardian")
    guardians = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('guardian.html', guardians=guardians)
