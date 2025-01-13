CREATE TABLE Guardian (
    GuardianID INT AUTO_INCREMENT PRIMARY KEY,
    GuardianName VARCHAR(100) NOT NULL,
    GuardianContact VARCHAR(15) UNIQUE NOT NULL
);

-- Create Location Table
CREATE TABLE Location (
    LocationID INT AUTO_INCREMENT PRIMARY KEY,
    GuardianID INT NOT NULL,
    City VARCHAR(50) NOT NULL,
    State VARCHAR(50) NOT NULL,
    ZipCode VARCHAR(10) NOT NULL,
    FOREIGN KEY (GuardianID) REFERENCES Guardian(GuardianID)
);

-- Create Child Table
CREATE TABLE Child (
    ChildID INT AUTO_INCREMENT PRIMARY KEY,
    GuardianID INT NOT NULL,
    ChildName VARCHAR(100) NOT NULL,
    ChildDOB DATE NOT NULL,
    ChildAge INT,
    ChildGender ENUM('M', 'F') NOT NULL,
    Allergies VARCHAR(255),
    FOREIGN KEY (GuardianID) REFERENCES Guardian(GuardianID)
);

-- Create Date Table for Vaccination Dates
CREATE TABLE Date (
    DateID INT AUTO_INCREMENT PRIMARY KEY,
    ChildID INT NOT NULL,
    FirstDate DATE,
    FOREIGN KEY (ChildID) REFERENCES Child(ChildID)
);

-- Create Hospital Table
CREATE TABLE Hospital (
    HospitalID INT AUTO_INCREMENT PRIMARY KEY,
    H_Name VARCHAR(100) NOT NULL,
    H_Contact VARCHAR(15) NOT NULL,
    H_Email VARCHAR(100) NOT NULL
);

-- Create Vaccine Table
CREATE TABLE Vaccine (
    VaccineID INT AUTO_INCREMENT PRIMARY KEY,
    VaccineName VARCHAR(100) NOT NULL,
    RecommendedAgeRange VARCHAR(50),
    Exclusions VARCHAR(255),
    V_Cost DECIMAL(10, 2) NOT NULL,
    HospitalID INT NOT NULL,
    FOREIGN KEY (HospitalID) REFERENCES Hospital(HospitalID)
);

CREATE TABLE Consent (
    ConsentID INT AUTO_INCREMENT PRIMARY KEY,  -- Automatically incrementing primary key
    ChildID INT NOT NULL,                      -- Foreign key, must be provided
    VaccineID INT NOT NULL,                    -- Foreign key, must be provided
    DateGiven DATE NOT NULL,                   -- Date when consent was given
    Sign TINYINT(1) DEFAULT 0,                 -- 0 for No, 1 for Yes (BOOLEAN equivalent)
    AdditionalNotes VARCHAR(255),              -- Notes for additional information
    FOREIGN KEY (ChildID) REFERENCES Child(ChildID),  -- Maintain referential integrity
    FOREIGN KEY (VaccineID) REFERENCES Vaccine(VaccineID),
    UNIQUE (ChildID, VaccineID)                -- Ensure unique consent per child and vaccine
);



-- Create VaccinationHistory Table
CREATE TABLE VaccinationHistory (
    VaccinationHistoryID INT AUTO_INCREMENT PRIMARY KEY,
    ChildID INT NOT NULL,
    VaccineID INT NOT NULL,
    FirstDate DATE NOT NULL,
    LotNumber VARCHAR(50),
    Provider VARCHAR(100),
    LocationID INT NOT NULL,
    FOREIGN KEY (ChildID) REFERENCES Child(ChildID),
    FOREIGN KEY (VaccineID) REFERENCES Vaccine(VaccineID),
    FOREIGN KEY (LocationID) REFERENCES Location(LocationID)
);

-- Create Inventory Table
CREATE TABLE Inventory (
    InvID INT AUTO_INCREMENT PRIMARY KEY,
    Inv_Name VARCHAR(100) NOT NULL,
    Inv_Contact VARCHAR(15) NOT NULL,
    QuantityRemaining INT NOT NULL,
    HospitalID INT NOT NULL,
    FOREIGN KEY (HospitalID) REFERENCES Hospital(HospitalID)
);

-- Create VaccineInventoryLocation Table
CREATE TABLE VaccineInventoryLocation (
    LocationID INT AUTO_INCREMENT PRIMARY KEY,
    InvID INT NOT NULL,
    City VARCHAR(50) NOT NULL,
    State VARCHAR(50) NOT NULL,
    ZipCode VARCHAR(10) NOT NULL,
    FOREIGN KEY (InvID) REFERENCES Inventory(InvID)
);