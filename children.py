from flask import Blueprint, render_template
from db import get_db_connection  # Import from db.py

children_bp = Blueprint('children', __name__)

@children_bp.route('/children', methods=['GET'])
def view_children():
    conn = get_db_connection()
    if conn is None:
        return "Database connection failed.", 500

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT c.ChildID, c.ChildName, c.ChildDOB, c.ChildGender, g.GuardianName, c.Allergies, c.ChildAge
        FROM Child c
        JOIN Guardian g ON c.GuardianID = g.GuardianID
    """)
    children = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('children.html', children=children)

