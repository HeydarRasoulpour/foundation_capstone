# Competency Tracking Tool

A console-based Python application for tracking competencies, managing users, and recording assessment results. Designed for use by both regular users and managers.

## Features

- Secure login system with role-based access (User and Manager)
- Create: Add new records (adding a new user, new competency, new assessment and assessment result.)
- Read: View or retrieve existing records (viewing users, competencies, assessments and assessment results)
- Update: Edit existing records (Edite users, competencies, assessments and assessment results)
- Delete: Remove records (deleting an old assessment result by manager)
- CSV import/export functionality
- Reporting on user progress and assessments

## Usage Instructions

### 1. Start the Application

Run the following command in your terminal:

python capstone.py

### 2. Login

You’ll be prompted to log in with your email and password.

If you’re a Manager, you’ll have access to full administrative features.

If you’re a Regular User, you’ll see a limited menu to view and edit your own data.

### 3. Main Menu Options
Depending on your role, you'll see different options.

#### If you're a User:
Please select from the options:
    1. View Competency and Assessment Data
    2. Change First Name and Last Name
    3. Change Phone Number
    4. Change Email
    5. Change Password
    6. Log Out

#### If you're a Manager:
Please select from the options:
    1. View all users
    2. Search for user
    3. View all users' competency levels for a competency
    4. View competency level report for a user
    5. View a list of assessments for a user
    6. Add User
    7. Add new competency
    8. Add new assessment to competency
    9. Add assessment result for user
    10. Edit user information
    11. Edit competency
    12. Edit assessment
    13. Edit assessment result
    14. Delete assessment result
    15. Import assessment results from CSV
    16. Log out

### 4. How to Perform Common Actions (Manager only)
#### -View all users: Type 1 in the console and press Enter. 
#### -To search for a user:
    Type 2 in the console and press Enter
    When prompted, enter the user's name 
#### -View all users' competency levels:
    Type 3 in the console and press Enter
    Enter the Competency ID when prompted
    A CSV report will be generated and saved using the competency name
#### -View competency level report for a user:
    Type 4 in the console and press Enter
    Enter the user ID when prompted
    A CSV report will be generated and saved using the user's name
#### -View a list of assessments for a user:
    Type 5 in the console and press Enter
    Enter the User ID when prompted
    The list of assessments will be displayed in the console
#### - Add a New User :
    Type 6 in the console and press Enter to select "Add New User"
    Enter the required details (name, email, role, etc.)    
    After submission, a list of all users will be displayed in the console
#### -Add new competency:
    Type 7 in the console and press Enter
    Enter the competency name 
    The Competency ID and date will be generated automatically
#### -Add new assessment to competency:
    Type 8 in the console and press Enter
    Enter the Competency ID
    Enter the assessment name
    Enter the assessment type  
    The assessment ID and date will be generated automatically
#### -Add assessment result for user:
    Type 9 in the console and press Enter
    Enter the User ID
    Enter the Assessment ID
    Enter the user's Score (0 to 4)
    Enter the Date Taken (YYYY-MM-DD)
    Enter the Manager ID (who administered the assessment)
#### -Edit user information:
    Type 10 in the console and press Enter
    Enter the User ID of the user you want to edit
    Select the field to update from the menu:
        1. First Name and Last Name
        2. Phone Number
        3.Email
        4. Password
        5. Role
        6. Active
        7. Exit
    Enter the new information when prompted
#### -Edit competency:
    Type 11 in the console and press Enter
    Enter competency ID to edit
    Enter new competency Name to update
#### -Edit assessment:
    Type 12 in the console and press Enter
    Enter assessment ID to edit
    Select the field to update from the menu:    
        1. Update Competency ID
        2. Update Assessment Name
        3. Update Assessment Type
    Enter the new information when prompted
#### -Edit assessment result:
    Type 13 in the console and press Enter
    Enter Result ID to edit
    Select the field to update from the menu:
        1. Update User ID
        2. Update Assessment ID
        3. Update Score
        4. Update Manager ID
    Enter the new information when prompted
#### -Delete assessment result:
    Type 14 in the console and press Enter
    Enter the Result ID to delete
    Review the displayed information
    Enter 1 to confirm and delete the result
#### -Import assessment results from CSV:
    Type 15 in the console and press Enter
    Enter the CSV directory path and the CSV file name when prompted
#### -Log out:
    Type 16 in the console and press Enter

### 5. How to Perform Common Actions (User)
#### -View Competency and Assessment Data:
    Type 1 in the console and press Enter
    Enter the user ID when prompted
    Assessment Results for the user will desplay
#### -Change First Name and Last Name:
    Type 2 in the console and press Enter
    Enter new Name
    Enter New Last Name
#### -Change Phone Number:
    Type 3 in the console and press Enter
    Enter New Phone Number
#### -Change Email:
    Type 4 in the console and press Enter
    Enter Nwe Email
#### -Change Password:
    Type 5 in the console and press Enter
    Enter New password
#### -Log Out:
    Type 6 in the console and press Enter



