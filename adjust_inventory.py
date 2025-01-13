
from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import get_db_connection  # Import from db.py

adjust_inventory_bp = Blueprint('adjust_inventory', __name__)

@adjust_inventory_bp.route('/adjust-inventory', methods=['GET', 'POST'])
def adjust_inventory():
    conn = get_db_connection()
    if conn is None:
        flash("Database connection failed. Please try again later.", 'danger')
        return redirect(url_for('home'))

    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        vaccine_id = request.form['vaccine_id']
        quantity_to_add = int(request.form['quantity_to_add'])  # Get the quantity to add

        try:
            # Fetch the current quantity
            cursor.execute("SELECT QuantityRemaining FROM Inventory WHERE InvID = %s", (vaccine_id,))
            result = cursor.fetchone()

            if result:
                current_quantity = result['QuantityRemaining']
                updated_quantity = current_quantity + quantity_to_add

                # Update the quantity in the database
                cursor.execute(
                    "UPDATE Inventory SET QuantityRemaining = %s WHERE InvID = %s",
                    (updated_quantity, vaccine_id)
                )
                conn.commit()
                flash(f'Inventory updated successfully! New quantity: {updated_quantity}', 'success')
            else:
                flash('Vaccine not found in inventory.', 'danger')

        except Exception as e:
            flash(f'An error occurred: {e}', 'danger')
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('inventory.view_inventory'))

    # Fetch vaccine options for the dropdown
    cursor.execute("SELECT VaccineID, VaccineName FROM Vaccine")
    vaccines = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('adjust_inventory.html', vaccines=vaccines)

