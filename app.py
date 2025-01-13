from flask import Flask, render_template
import mysql.connector
from blueprints.add_child import add_child_bp
from blueprints.add_guardian import add_guardian_bp
from blueprints.add_vaccine import add_vaccine_bp
from blueprints.add_vaccination import add_vaccination_bp
from blueprints.adjust_inventory import adjust_inventory_bp
from blueprints.children import children_bp
from blueprints.guardians import guardians_bp
from blueprints.consent_form import consent_bp
from blueprints.inventory import inventory_bp
from blueprints.vaccines import vaccines_bp
from blueprints.vaccination_history import vaccination_history_bp

app = Flask(__name__)
app.secret_key='surtur@123'
# Define the function to establish a database connection
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',             # Replace with your MySQL username
            password='kaddu@123', # Replace with your MySQL password
            database='dbms_project' # Replace with your database name
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Register blueprints for modular routing
app.register_blueprint(add_child_bp)
app.register_blueprint(add_guardian_bp)
app.register_blueprint(add_vaccine_bp)
app.register_blueprint(add_vaccination_bp)
app.register_blueprint(adjust_inventory_bp)
app.register_blueprint(children_bp)
app.register_blueprint(guardians_bp)
app.register_blueprint(consent_bp)
app.register_blueprint(inventory_bp)
app.register_blueprint(vaccines_bp)
app.register_blueprint(vaccination_history_bp)

# Main route to the home page or dashboard
@app.route('/')
def home():
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)
