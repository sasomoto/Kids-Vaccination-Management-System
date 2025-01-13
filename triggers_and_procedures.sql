-- Triggers and Procedures for Kids Vaccination Management System

-- SECTION 1: TRIGGERS

-- 1. Prevent duplicate vaccinations with a minimum interval
DELIMITER //

CREATE TRIGGER trg_prevent_duplicate_vaccination
BEFORE INSERT ON VaccinationHistory
FOR EACH ROW
BEGIN
    DECLARE v_last_vaccination_date DATE;
    
    SELECT MAX(FirstDate) INTO v_last_vaccination_date
    FROM VaccinationHistory
    WHERE ChildID = NEW.ChildID AND VaccineID = NEW.VaccineID;

    IF v_last_vaccination_date IS NOT NULL AND (DATEDIFF(CURRENT_DATE, v_last_vaccination_date) < 28) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'The child must wait 28 days between doses of the same vaccine.';
    END IF;
END;
//

-- 2. Reduce inventory on vaccination
CREATE TRIGGER trg_reduce_inventory_on_vaccination
AFTER INSERT ON VaccinationHistory
FOR EACH ROW
BEGIN
    DECLARE current_quantity INT;
    
    SELECT QuantityRemaining INTO current_quantity
    FROM Inventory
    WHERE InvID = (SELECT InvID FROM Vaccine WHERE VaccineID = NEW.VaccineID);

    IF current_quantity > 0 THEN
        UPDATE Inventory
        SET QuantityRemaining = QuantityRemaining - 1
        WHERE InvID = (SELECT InvID FROM Vaccine WHERE VaccineID = NEW.VaccineID);
    ELSE
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Insufficient inventory for the selected vaccine.';
    END IF;
END;
//

-- 3. Log inventory changes
CREATE TABLE InventoryLog (
    LogID INT AUTO_INCREMENT PRIMARY KEY,
    InvID INT NOT NULL,
    `Change` INT NOT NULL,
    ChangeDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (InvID) REFERENCES Inventory(InvID)
);

CREATE TRIGGER trg_log_inventory_changes
AFTER UPDATE ON Inventory
FOR EACH ROW
BEGIN
    INSERT INTO InventoryLog (InvID, `Change`)
    VALUES (OLD.InvID, NEW.QuantityRemaining - OLD.QuantityRemaining);
END;
//

-- 4. Log consent changes
CREATE TABLE ConsentLog (
    LogID INT AUTO_INCREMENT PRIMARY KEY,
    ConsentID INT,
    ChangeDate DATE,
    OldSign TINYINT,
    NewSign TINYINT
);

CREATE TRIGGER trg_log_consent_changes
AFTER UPDATE ON Consent
FOR EACH ROW
BEGIN
    IF OLD.Sign != NEW.Sign THEN
        INSERT INTO ConsentLog (ConsentID, ChangeDate, OldSign, NewSign)
        VALUES (OLD.ConsentID, CURDATE(), OLD.Sign, NEW.Sign);
    END IF;
END;
//

-- SECTION 2: STORED PROCEDURES

-- 1. Register a new child
CREATE PROCEDURE pr_register_child(
    IN p_guardian_id INT,
    IN p_child_name VARCHAR(255),
    IN p_child_dob DATE,
    IN p_gender CHAR(1),
    IN p_allergies VARCHAR(255)
)
BEGIN
    INSERT INTO Child (GuardianID, ChildName, ChildDOB, ChildGender, Allergies)
    VALUES (p_guardian_id, p_child_name, p_child_dob, p_gender, p_allergies);
    COMMIT;
END;
//

-- 2. Add new vaccine inventory
CREATE PROCEDURE pr_add_vaccine_inventory(
    IN p_inv_name VARCHAR(255),
    IN p_inv_contact VARCHAR(255),
    IN p_quantity INT,
    IN p_hospital_id INT
)
BEGIN
    INSERT INTO Inventory (Inv_Name, Inv_Contact, QuantityRemaining, HospitalID)
    VALUES (p_inv_name, p_inv_contact, p_quantity, p_hospital_id);
    COMMIT;
END;
//

-- 3. Adjust vaccine cost and log changes
CREATE TABLE VaccineCostLog (
    LogID INT AUTO_INCREMENT PRIMARY KEY,
    VaccineID INT,
    DateChanged DATE,
    OldCost DECIMAL(10, 2),
    NewCost DECIMAL(10, 2)
);

CREATE PROCEDURE pr_adjust_vaccine_cost(
    IN p_vaccine_id INT,
    IN p_new_cost DECIMAL(10,2)
)
BEGIN
    DECLARE v_old_cost DECIMAL(10,2);
    
    SELECT V_Cost INTO v_old_cost FROM Vaccine WHERE VaccineID = p_vaccine_id;

    UPDATE Vaccine SET V_Cost = p_new_cost WHERE VaccineID = p_vaccine_id;

    INSERT INTO VaccineCostLog (VaccineID, DateChanged, OldCost, NewCost)
    VALUES (p_vaccine_id, CURDATE(), v_old_cost, p_new_cost);

    COMMIT;
END;
//

-- 4. Retrieve child vaccination history
CREATE PROCEDURE pr_get_child_vaccination_history(
    IN p_child_id INT
)
BEGIN
    SELECT 
        v.VaccineName,
        vh.FirstDate,
        IFNULL(vh.SecondDate, 'Not Given') as SecondDate,
        vh.Provider
    FROM VaccinationHistory vh
    JOIN Vaccine v ON vh.VaccineID = v.VaccineID
    WHERE vh.ChildID = p_child_id;
END;
//

-- SECTION 3: FUNCTIONS

-- 1. Calculate total vaccine cost for a child
CREATE FUNCTION fn_calculate_total_vaccine_cost(p_child_id INT)
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE v_total_cost DECIMAL(10,2);
    
    SELECT COALESCE(SUM(v.V_Cost), 0) INTO v_total_cost
    FROM VaccinationHistory vh
    JOIN Vaccine v ON vh.VaccineID = v.VaccineID
    WHERE vh.ChildID = p_child_id;

    RETURN v_total_cost;
END;
//

-- 2. Get guardian contact
CREATE FUNCTION fn_get_guardian_contact(p_child_id INT)
RETURNS VARCHAR(15)
DETERMINISTIC
BEGIN
    DECLARE v_contact VARCHAR(15);
    
    SELECT g.GuardianContact INTO v_contact
    FROM Guardian g
    JOIN Child c ON g.GuardianID = c.GuardianID
    WHERE c.ChildID = p_child_id;

    RETURN v_contact;
END;
//

-- 3. Check inventory availability
CREATE FUNCTION fn_check_inventory(p_vaccine_id INT)
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE v_quantity INT;
    
    SELECT QuantityRemaining INTO v_quantity
    FROM Inventory
    WHERE InvID = (SELECT InvID FROM Vaccine WHERE VaccineID = p_vaccine_id);

    RETURN COALESCE(v_quantity, 0);
END;
//

DELIMITER;