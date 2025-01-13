from flask import Blueprint, render_template
from db import get_db_connection  # Import from db.py

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/inventory', methods=['GET'])
def view_inventory():
    conn = get_db_connection()
    if conn is None:
        return "Database connection failed.", 500

    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT InvID, Inv_Name, Inv_Contact, QuantityRemaining, HospitalID FROM Inventory")
    inventory = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('inventory.html', inventory=inventory)

