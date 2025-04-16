

import sqlite3
import bcrypt
from datetime import datetime
import csv

def db_connection(): 
    try:
        connection = sqlite3.connect("competency.db")
        cursor = connection.cursor()
        return connection, cursor
    except Exception as e:
        print(f'Database connection failed:{e}')


def create_schema():
    try:
        connection, cursor = db_connection() 
        with open ('tables.txt', 'r') as my_table:
            read_tables = my_table.read()
            cursor.executescript(read_tables)     
        connection.commit()
    except Exception as e:
        print(f"Adding tables failed: {e}")



def safe_input(prompt):
    user_input = input(prompt).strip()
    if user_input.lower() == 'q':
        print("User cancelled the operation.")
        return None
    return user_input

def dynamic_printing(data):
    new_data = []
    for row in data:
        new_row = []
        for item in row:
            new_row.append(str(item))
        new_data.append(new_row)

    data = new_data
    column_widths = []
    for column_index in range(len(data[0])):
        max_width = 0
        for row in data:
            iteam_length = len(row[column_index])
            if iteam_length > max_width:
                max_width = iteam_length
        column_widths.append(max_width)

    for row in data:
        row_items = []
        for i, value in enumerate(row):
            formated_value = str(value).ljust(column_widths[i])
            row_items.append(formated_value)
        print("  ".join(row_items))



class Users:
    

    def __init__(self, user_id, first_name, last_name, phone_number, email, password, hiring_date, role, active):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.email = email
        self.date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.password = password
        self.hiring_date = hiring_date
        self.role = role
        self.active = active

    
    
    def hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    
    def log_in(self, email, password):
         
        self.email = email
        
        self.password = password
        
        if not email:
            print(" Please enter your email.")
            return False
        
        cursor = connection.cursor()
        try:
            result = cursor.execute("SELECT user_id, password, role , active FROM Users WHERE email = ? ;" , (email,)).fetchone()
        except Exception as e:
            print(f"Error retrieving results: {e}")
            return
        if not result:
            print("User not found.")
            return False
        
        user_id, saved_password, role, active = result
        if active == 0:
            print("Your access has been denied.")
            return

        if isinstance(saved_password, str):
            saved_password = saved_password.encode('utf-8') # Encode if it's a string / Ensure it's in bytes
        
        if bcrypt.checkpw(password.encode('utf-8'), saved_password): # Check if the password matches
            print("User found")
            return user_id, role.lower()
        
        else:
            print("Incorrect password.")
            return False
    

    def add_user_to_db(self):
        while True:
            print("\n=== Add New User ===")
            try:
                while True:
                    first_name_input = safe_input("please input First Name(Type q to return to main menu):")
                    if first_name_input is None:
                        return
                    if not first_name_input:
                        print("First name cannot be empty.")
                        continue
                    if not first_name_input.isalpha():
                        print("First name should contain only letters.") 
                        continue  
                    self.first_name = first_name_input.capitalize()
                    break

                while True:
                    last_name_input = safe_input("Please input Last Name(Type q to return to main menu): ")
                    if last_name_input is None:
                        return
                    if not last_name_input:
                        print("Last name cannot be empty.")
                        continue
                    if not last_name_input.isalpha():
                        print("Last name should contain only letters.")
                        continue
                    self.last_name = last_name_input.capitalize()
                    break
                while True:
                    phone_number_input = safe_input("please input phone number(Type q to return to main menu):")
                    if phone_number_input is None:
                        return
                    if not phone_number_input.isdigit():
                        print("Phone number must be numeric")
                        continue                       
                    if len(phone_number_input) != 10:
                        print("Phone number must be 10 digit characters")
                        continue
                    self.phone_number = phone_number_input
                    break
                
                while True:
                    email_input = safe_input("please input Email(Type q to return to main menu):")
                    if email_input is None:
                        return                   
                    if "@" not in email_input:
                        print("Email must contain '@'")
                        continue
                    if '.' not in email_input.split("@")[-1]:
                        print("Email must contain a domain like '.com'")
                        continue
                    if not email_input:
                        print("Email cannot be empty.")
                        continue
                    self.email = email_input
                    break

                self.date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                while True:
                    password = safe_input ("please input password here(Type q to return to main menu):")
                    if password is None:
                        return
                    if len(password) < 8:
                        print("Password must be at least 8 characters long.")
                        continue
                    if not password:
                        print("Password cannot be empty.")
                        continue
                    self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                    break
                while True:
                    hiring_date_input = safe_input("please input hiring date(YYYY-MM-DD)(Type q to return to main menu):")
                    if hiring_date_input is None:
                        return
                    if not hiring_date_input:
                        print("Hiring date cannot be empty.")
                        continue
                    try:
                        datetime.strptime(hiring_date_input, "%Y-%m-%d")
                        self.hiring_date = hiring_date_input
                        break
                    except ValueError:
                        print("Hiring date must be in YYYY-MM-DD format.")
                        continue
                    
                while True:
                    role_input = safe_input("please input role(Type q to return to main menu):")
                    if role_input is None:
                        return
                    role_input = role_input.capitalize()
                    if role_input not in ['User', 'Manager']:
                        print("Role must be 'User' or 'Manager'.")
                        continue
                    self.role = role_input
                    break
                while True:
                    active_input = safe_input("Is the user Active? 1 = Yes or 0 = No (Type q to return to main menu):")
                    if active_input is None:
                        return
                    if active_input not in ["0","1"]:
                        print("Active must be either 0 or 1.")
                        continue
                    self.active = active_input
                    break

                connection, cursor = db_connection()
                
                query = """INSERT INTO Users(first_name, last_name, phone, email, date_created, password, hiring_date, role, active) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?);""" 
                values = (self.first_name, self.last_name, self.phone_number, self.email, self.date_created, self.password.decode('utf-8'), self.hiring_date, self.role, self.active)

                cursor.execute(query, values) 
                connection.commit()
                print("User saved successfully!")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
    

                
    def edit_name(self):
        while True:
            # self.user_id = user_id
            self.first_name_input = safe_input("Enter new first name(Type q to return to main menu): ")
            
            if self.first_name_input is None:
                return
            if not self.first_name_input:
                print("This field cannot be left blank.")
                continue
            if not self.first_name_input.isalpha():
                print("First name should contain only letters.") 
                continue 
            self.first_name_input = self.first_name_input.capitalize()
            
            self.last_name_input = safe_input("Enter new last name(Type q to return to main menu): ")
            if self.last_name_input is None:
                return
            if not self.last_name_input:
                print("This field cannot be left blank.")
                continue
            if not self.last_name_input.isalpha():
                print("First name should contain only letters.") 
                continue 
            self.last_name_input = self.last_name_input.capitalize()

            connection, cursor = db_connection()
            try:
                cursor.execute("UPDATE Users SET first_name = ?,last_name =? WHERE user_id = ?;", (self.first_name_input,self.last_name_input,self.user_id))
                connection.commit()
                print("Name updated successfully.")
            except Exception as e:
                print(f"Error Updating name {e}")
                continue 
            break


    def edit_phone(self):
        while True:
            self.phone_input = safe_input("Please input new phone number(Type q to return to main menu):")
            if self.phone_input is None:
                return
            if not self.phone_input.isdigit():
                print("Phone number must be numeric")
                continue
            if len(self.phone_input) != 10:
                print("Phone number must be 10 digit characters")
                continue

            connection, cursor = db_connection()
            try:
                cursor.execute("UPDATE Users SET phone = ? WHERE user_id = ?;", (self.phone_input, self.user_id))
                connection.commit()
                print("Phone number updated successfully.")
            except Exception as e:
                print(f"Error updating phone number: {e}")
                continue
            break

        
    def edit_email(self):
        while True: 
            self.email_input = safe_input("Please input new email(Type q to return to main menu):")
            if self.email_input is None:
                return
            if not self.email_input:
                print("This field cannot be left blank.")
                continue
            if "@" not in self.email_input:
                print("Email must contain '@'")
                continue
            if '.' not in self.email_input.split("@")[-1]:
                print("Email must contain a domain like '.com'")
                continue
            
            connection, cursor = db_connection()
            try:
                cursor.execute("UPDATE Users SET email = ? WHERE user_id = ?;", (self.email_input, self.user_id))
                connection.commit()
                print("Email updated successfully.")
            except Exception as e:
                print(f"Error updating email: {e}")
                continue
            break

                
    def edit_password(self):
        while True:
            password = safe_input("Please input new password(Type q to return to main menu):")
            if password is None:
                return
            if not password:
                print("This field cannot be left blank.")
                continue
            if len(password) < 8:
                print("Password must be at least 8 characters long.")
                continue
            self.password = self.hash_password(password)
            connection, cursor = db_connection()
            try:
                cursor.execute("UPDATE Users SET password = ? WHERE user_id = ?;", (self.password, self.user_id))
                connection.commit()
                print("Password updated successfully.")
            except Exception as e:
                print(f"Error updating password: {e}")
                continue
            break


    def edit_role(self):
        while True:
            self.role_input = safe_input("Please input new role(Type q to return to main menu):")
            if self.role_input is None:
                return
            self.role_input = self.role_input.capitalize()

            if self.role_input not in ['User', 'Manager']:
                print("Role must be 'User' or 'Manager'.")
                continue
                
            if not self.role_input:
                print("This field cannot be left blank.")
                return
            
            connection, cursor = db_connection()
            try:
                cursor.execute("UPDATE Users SET role = ? WHERE user_id = ?;", (self.role_input, self.user_id))
                connection.commit()                
                print("Role updated successfully.")
            except Exception as e:
                print(f"Error updating role: {e}")
                continue
            break
            

    def edit_active(self):
        while True:
            self.active_input = safe_input("Please input (1 for active) or (0 for deactive) user(Type q to return to main menu): ")
            if self.active_input is None:
                return
            self.active_input = self.active_input.strip()
            if self.active_input not in ['0', '1']:
                print("Invalid input. Please enter '1' for active or '0' for deactive.")
                continue
            
            connection, cursor = db_connection()
            try:
                cursor.execute("UPDATE Users SET active = ? WHERE user_id = ?;", (self.active_input, self.user_id))
                connection.commit()
                print("Active updated successfully.")
            except Exception as e:
                print(f"Error updating active status: {e}")
                continue
            break

        


def view_all_users():
    try:
        connection, cursor = db_connection()

        results = cursor.execute("SELECT * FROM Users;").fetchall()
        if not results:
            print("No users found in the database.")
            return
        header = (
            "User_id", "First Name", "Last Name", "Phone Number",
            "Email", "Date Created", "Hiring Date", "Role", "Active")

        data = [header]
        for row in results:
            data.append((
            row[0], row[1], row[2], row[3], row[4],
            row[5], row[7], row[8], row[9] ))

        dynamic_printing(data)

    except Exception as e:
        print(f"An error occurred: {e}")


def search_user_by_name():
    try:
        connection, cursor = db_connection()
        while True:
            user_id_input = safe_input("Please input name to search(Type q to return to main menu)")
            if user_id_input is None:
                return
            results = cursor.execute("SELECT * FROM Users WHERE first_name LIKE ? OR last_name LIKE ?", (f'%{user_id_input}%', f'%{user_id_input}%')).fetchall()
            if not results:
                print("No matches found.")
                continue
            
            print("\nMatching users:")
            header = (
                "User_id", "First Name", "Last Name", "Phone Number",
                "Email", "Date Created", "Hiring Date", "Role", "Active")

            data = [header]
            for row in results:
                data.append((
                row[0], row[1], row[2], row[3], row[4],
                row[5], row[7], row[8], row[9] ))

            dynamic_printing(data)
            break
    except Exception as e:
        print(f"An error occurred: {e}")
                
 
class Competencies:
    def __init__(self, competency_id, name):
        self.competency_id = competency_id
        self.name = name
        self.date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    
    def add_competency_to_db(self):
        while True:
            try:
                print("\n=== Add Competency ===")

                self.name = safe_input ("Please input competency name(Type q to return to main menu)")
                if self.name is None:
                    break
                self.name = self.name.capitalize()
                if not self.name:
                    print("Competency name can not be empty.")
                    continue

                connection, cursor = db_connection()
                
                query = """INSERT INTO Competencies(name, date_created) VALUES (
                ?, ?);""" 
                values = (self.name, self.date_created)

                cursor.execute(query, values) 
                connection.commit()
                print("Competency saved successfully!")
                break
            except Exception as e:
                print(f"An erroe occured: {e}")


    def update_competency(self):
        connection, cursor = db_connection()
        while True: 
            competency_id_input = safe_input ("Please input Competency ID to edit(Type q to return to main menu)")
            if competency_id_input is None:
                break
            
            if not competency_id_input.isdigit():
                print("Competency ID must be numeric")
                continue
            
            result = cursor.execute('select competency_id FROM Competencies WHERE competency_id =?;',(competency_id_input,)).fetchone()
            if not result:
                print("No assessment found with the provided Assessment ID.")
                continue    
            competency_name = safe_input ("Please input the Competency Name(Type quit or q to exit)")
            if competency_name is None:
                break
            competency_name = competency_name.strip()
            if not competency_name:
                print("Competency name can not be empty.")
                continue
            
            self.competency_id = competency_id_input
            self.name = competency_name.capitalize()
            try:
                
                cursor.execute("UPDATE Competencies SET name = ? WHERE competency_id = ?;", (self.name, self.competency_id))
                
                connection.commit()
                
                print("Competency updated successfully.")
                break
            except Exception as e:
                print(f'Error updating competency:{e}')



class Assessments:
    def __init__(self, assessment_id, competency_id, name, assessment_type):
        self.assessment_id = assessment_id
        self.competency_id = competency_id
        self.name = name
        self.assessment_type = assessment_type
        self.date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def add_assessment_to_competency(self):
        try:
            while True:
                competency_id_input = safe_input ("Please enter the Competency ID to add an assessment(Type q to return to main menu):")
                if competency_id_input is None:
                    return
               
                if not competency_id_input:
                    print("Competency ID can not be empty.")
                    continue
                if not competency_id_input.isdigit():
                    print("Competency ID must be number.")
                    continue
                break
            while True:
                name_input = safe_input ("Please enter the assessment name(Type q to return to main menu)")
                if name_input is None:
                    return
                if not name_input:
                    print("Assessment name can not be empty.")
                    continue
                break
            while True:
                assessment_type_input = safe_input ("""Please input (1 - 4) from the options(Type q to return to main menu):                                                    
                                                    1.Online Written Test
                                                    2.Online Quiz Test
                                                    3.Interview
                                                    4.Programming Assignment
                                                    """)
                if assessment_type_input == "1": assessment_type = "Online Written Test"
                if assessment_type_input == "2": assessment_type = "Online Quiz Test"
                if assessment_type_input == "3": assessment_type = "Interview"
                if assessment_type_input == "4": assessment_type = "Programming Assignment"
                

                if assessment_type_input is None:
                    return
                
                if not assessment_type_input:
                    print("Assessment type can not be empty.")
                    continue
                if assessment_type_input not in ["1", "2", "3","4"]:
                    print("Please select from the list")
                    continue
                break
            self.competency_id = competency_id_input
            self.name = name_input.capitalize()
            self.assessment_type = assessment_type

            connection, cursor = db_connection()
            
            query = """INSERT INTO Assessments(competency_id,name, assessment_type, date_created) VALUES (
            ?, ?,?,?);""" 
            values = (self.competency_id, self.name, self.assessment_type, self.date_created)

            cursor.execute(query, values) 
            connection.commit()
            print("Assessment saved successfully!")
            
        except Exception as e:
            print(f"Unexpected error: {e}")


    def edit_assessment(self):
        connection, cursor = db_connection()
        while True:
            self.assessment_id = safe_input("Please enter Assessment ID to edit(Type q to return to main menu)")
            if self.assessment_id is None:
                return
        
            if not self.assessment_id:
                print("Assessment ID can not be empty.")
                continue
            result = cursor.execute('select assessment_id FROM Assessments WHERE assessment_id =?;',(self.assessment_id,)).fetchone()
            if not result:
                print("No assessment found with the provided Assessment ID.")
                continue

            assessment_update = safe_input ("""Please select from list(1 - 3)(Type q to return to main menu)
                                    1.Update Competency ID
                                    2.Update Assessment Name
                                    3.Update Assessment Type """)
            if assessment_update is None:
                break
            
            if assessment_update not in ["1", "2", "3"]:
                print("Invalid selection. Please choose 1, 2, or 3.")
                continue
            break

        try:
            
            if assessment_update == "1":
                while True:
                    self.competency_id = safe_input ("Please enter new Competency ID to add an assessment(Type q to return to main menu).")
                    if self.competency_id is None:
                        break
                    
                    if not self.competency_id:
                        print("Competency ID cannot be empty.")
                        continue
                    if not self.competency_id.isdigit():
                        print("Competency ID must be number.")
                        continue   
                    cursor.execute("UPDATE Assessments SET competency_id = ? WHERE assessment_id = ?;", (self.competency_id, self.assessment_id))
                    connection.commit()
                    print("Competency_id updated successfully.")
                    break

            elif assessment_update == "2":
                while True:
                    self.name = safe_input ("Please enter new assessment name(Type q to return to main menu)")
                    if self.name is None:
                        break
                    self.name = self.name.capitalize()
                    if not self.name:
                        print("Assessment name cannot be empty.")
                        continue
                    cursor.execute("UPDATE Assessments SET name = ? WHERE assessment_id = ?;", (self.name, self.assessment_id))
                    connection.commit()               
                    print("Assessment Name updated successfully.")
                    break

            elif assessment_update == "3":
                while True:
                    self.assessment_type = safe_input ("Please enter new assessment type(Type q to return to main menu)")
                    if self.assessment_type is None:
                        break
                    self.assessment_type = self.assessment_type.capitalize()
                    if not self.assessment_type:
                        print("Assessment type can not be empty.")
                        continue                    
                    cursor.execute("UPDATE Assessments SET assessment_type = ? WHERE assessment_id = ?;", (self.assessment_type, self.assessment_id))
                    connection.commit()
                    print("Assessment Type updated successfully.")
                    break
        except Exception as e:
            print(f"Unexpected error: {e}")


def list_user_competency_assessments():
    try:
        connection, cursor = db_connection()
        while True:
            user_id = safe_input("please input user_id(Type q to return to main menu)")
            if user_id is None:
                break

            if not user_id.isdigit():
                print("Invalid input. Please enter a numeric user_id.")
                continue
            try:
                results =cursor.execute("""SELECT Assessment_Results.result_id, Competencies.name, Assessments.name, Assessment_Results.score ,Assessments.date_created
                FROM Competencies JOIN Assessments
                ON Competencies.competency_id = Assessments.competency_id
                JOIN Assessment_Results
                ON Assessments.assessment_id = Assessment_Results.assessment_id
                WHERE Assessment_Results.user_id = ?; """, (user_id,)).fetchall()

                if not results:
                    print(f"No assessment results found for user_id {user_id}.\n")
                else:
                    print(f"\nAssessment Results for User {user_id}:")
                    header = (
                    "Result ID", "Competency Name", "Assessment Name", "Result Score", "Assessment Date Created")

                    data = [header]
                    for row in results:
                        data.append((
                        row[0], row[1], row[2], row[3], row[4]))

                    dynamic_printing(data)   
                    break

            except Exception as query_error:
                print(f"An error occurred while fetching data: {query_error}")
                break
    except Exception as e:
        print(f"An error occurred while fetching data: {e}")
    


class Assessment_results:
    def __init__(self,user_id, assessment_id, score,assessment_date, manager_id):
        self.user_id = user_id
        self.assessment_id = assessment_id
        self.score = score
        self.assessment_date = assessment_date
        self.manager_id = manager_id

    def add_assessment_result (self): 
        connection, cursor = db_connection()
        while True:
            user_id_input = safe_input ("Please enter the User ID(Type q to return to main menu):")
            if user_id_input is None:
                return
            
            if not user_id_input.isdigit():
                print("Invalid input. User ID must be a number.")
                continue
            result = cursor.execute('SELECT user_id FROM Users WHERE user_id =?;',(user_id_input,)).fetchone()
            if not result:
                print("No user found with the provided User ID.")
                continue
            self.user_id =int(user_id_input)
            break
        while True:
            assessment_id_input = safe_input ("Please enter the Assessment ID (Type q to return to main menu):")
            if assessment_id_input is None:
                return
            
            if not assessment_id_input.isdigit():
                print("Invalid input. Assessment ID must be a number.")
                continue
            result = cursor.execute('SELECT assessment_id FROM Assessments WHERE assessment_id =?;',(assessment_id_input,)).fetchone()
            if not result:
                print("No assessment found with the provided Assessment ID.")
                continue
            self.assessment_id = int(assessment_id_input)
            break
        while True:
            score_input = safe_input ("Please enter user's Score(0 - 4)(Type q to return to main menu):")
            if score_input is None:
                return
            
            if not score_input.isdigit():
                print("Invalid input. Score must be a number.")
                continue
            score = int(score_input)

            if score < 0 or score > 4:
                print("Score must be between 0 and 4.")
                continue
            self.score = score
            break
        while True:
            assessment_date_input = safe_input("Date Taken (YYYY-MM-DD)(Type q to return to main menu): ")
            if assessment_date_input is None:
                return
            
            try:
                datetime.strptime(assessment_date_input, "%Y-%m-%d")
            except Exception as e:
                print("Invalid date format. Use YYYY-MM-DD.{e}")
                continue
            self.assessment_date = assessment_date_input
            break

        while True:
            manager_id_input = safe_input ("Please enter Manager ID (who administered)(Type q to return to main menu): ")
            if manager_id_input is None:
                return
            
           
            if not manager_id_input.isdigit():
                print(f"Invalid input. Manager ID must be a number.")
                continue
            result = cursor.execute('SELECT user_id, role FROM Users WHERE user_id =? AND role =?;',(manager_id_input,"Manager")).fetchone()
            if not result:
                print("No manager found with the provided User ID.")
                continue
            self.manager_id = int(manager_id_input)
            break
        try:
            query = ("INSERT INTO Assessment_Results(user_id, assessment_id, score, assessment_date, manager_id)VALUES(?, ?, ?, ?,?)")
            values = (self.user_id, self.assessment_id, self.score, self.assessment_date, self.manager_id)
            cursor.execute(query, values)
            connection.commit()
            print("Assessment Result saved successfully!")
            
        except Exception as e:
            print(f"Error inserting values to database: {e}")
            return
        

    def edit_assessment_result(self): 
        connection, cursor = db_connection()
        while True:
            try:
                self.result_id = safe_input("Please enter Result ID to edit (Type q to return to main menu)")
                if self.result_id is None:
                    break
                if not self.result_id.isdigit():
                    print("Invalid Result ID. It must be numeric.")
                    continue
                result = cursor.execute("SELECT result_id FROM Assessment_Results WHERE result_id = ?;", (self.result_id,)).fetchone()
                if not result:
                    print("No Result found with the provided Result ID.")
                    continue
                result_update = safe_input ("""Please select from list(1 - 4)(Type q to return to main menu):
                                        1.Update User ID
                                        2.Update Assessment ID
                                        3.Update Score
                                        4.Update Manager ID """)
                if result_update is None:
                    break
                result_update = result_update.strip()
                if result_update not in ["1", "2", "3","4"]:
                    print("Invalid selection. Please choose 1, 2, 3 or 4")
                    continue
                if result_update == "1":
                    while True:
                        self.user_id = safe_input ("Please enter new User ID(Type q to return to main menu):")
                        if self.user_id is None:
                            return

                        if not self.user_id.isdigit():
                            print("Invalid User ID. It must be numeric.")
                            continue
                        result = cursor.execute('SELECT user_id FROM Users WHERE user_id =?;',(self.user_id,)).fetchone()
                        if not result:
                            print("No user found with the provided User ID.")
                            continue
                        cursor.execute("UPDATE Assessment_Results SET user_id = ? WHERE result_id = ?;", (self.user_id, self.result_id))                   
                        print("User ID updated successfully.")
                        break
                elif result_update == "2":
                    while True:
                        self.assessment_id = safe_input ("Please enter new Assessment ID(Type q to return to main menu):")
                        if self.assessment_id is None:
                            return
                        
                        if not self.assessment_id.isdigit():
                            print("Invalid Assessment ID. It must be numeric.")
                            continue
                        result = cursor.execute('SELECT assessment_id FROM Assessments WHERE assessment_id =?;',(self.assessment_id,)).fetchone()
                        if not result:
                            print("No assessment found with the provided Assessment ID.")
                            continue

                        cursor.execute("UPDATE Assessment_Results SET assessment_id = ? WHERE result_id = ?;", (self.assessment_id, self.result_id))                    
                        print("Assessment ID updated successfully.")
                        break
                elif result_update == "3":
                    while True:
                        self.score = safe_input ("Please enter new Score(Type q to return to main menu):")
                        if self.score is None:
                            return
                        if self.score < 0 or self.score > 4:
                            print("Score must be between 0 and 4.")
                            continue
                        
                        if not self.score.isdigit():
                            print("Invalid score. It must be a number.")
                            continue
                        self.score = float(self.score)
                        cursor.execute("UPDATE Assessment_Results SET score = ? WHERE result_id = ?;", (self.score, self.result_id))
                        
                        print("Score updated successfully.")
                        break
                elif result_update == "4":
                    while True:
                        self.manager_id = safe_input ("Please enter new Manager ID(Type q to return to main menu):")
                        if self.manager_id is None:
                            return
                        manager_id_check = cursor.execute("""SELECT user_id FROM Users WHERE user_id = ?;""",(self.manager_id))
                        if not manager_id_check:
                            print("No manager found with peovided manager Id")
                        
                        if not self.manager_id.isdigit():
                            print("Invalid Manager ID. It must be numeric.")
                            continue
                        result = cursor.execute('SELECT user_id, role FROM Users WHERE user_id =? AND role =?;',(self.manager_id,"Manager")).fetchone()
                        if not result:
                            print("No manager found with the provided User ID.")
                            continue
                        cursor.execute("UPDATE Assessment_Results SET manager_id = ? WHERE result_id = ?;", (self.manager_id, self.result_id))                   
                        print("Manager ID updated successfully.")
                        break
                connection.commit()
            except Exception as e:
                print(f"An error occurred: {e}")

    
    
    def delete_assessment_result(self):
        
            connection, cursor = db_connection()
            while True:
                try:
                    self.result_id = safe_input("Select result_id to delete(Type q to return to main menu):")
                    if self.result_id is None:
                        break
                   
                    result = cursor.execute("""SELECT Users.first_name, Users.last_name, Assessment_Results.* 
                                            FROM Users JOIN Assessment_Results
                                                ON Users.user_id = Assessment_Results.user_id
                                            WHERE result_id =?;""",(self.result_id,)).fetchone()
                    if not result:
                        print("No Assessment Result found with the provided Result ID.")
                        continue
                    print(f"First Name: {result[0]}\nLast Name: {result[1]}\nResult_id: {result[2]}\nUser_id: {result[3]}\nAssessment_id: {result[4]}\nScore: {result[5]}\nAssessment Date: {result[6]}\n")
                    user_confirmation = safe_input("please input (1 to continue) or (q to Exit)")
                    if user_confirmation == "1":
                        cursor.execute("""DELETE FROM Assessment_results WHERE result_id = ? ;""",(self.result_id,))   
                        connection.commit()
                        print(f"Result ID {self.result_id} has been removed successfully.")
                        break
                except Exception as e:
                    print("An error occurred: {e}")

    
    
def user_competency_summary():
    try:
        connection, cursor = db_connection()
    except Exception as e:
        print(f'Database connection failed:{e}')

    user_id = safe_input("Please enter  User ID to generate the report(Type q to return to main menu)")
    if user_id is None:
        return
    
    if not user_id.isdigit():
        print("Invalid input. Competency ID must be a number.")
        return
    try:
        user = cursor.execute("SELECT first_name, last_name, email FROM users WHERE user_id = ?", (user_id,)).fetchone()
       
    except Exception as e:
        print(f"Error retrieving results: {e}")
    if not user:
        print("No results found for the given user ID.")
        return
    try:
        results = cursor.execute("""SELECT Competencies.name, COALESCE(Assessment_Results_Latest.score, 0)
            FROM Competencies
            LEFT JOIN Assessments 
                ON Assessments.competency_id = Competencies.competency_id
            LEFT JOIN (
                SELECT Assessment_Results.*
                FROM Assessment_Results
                INNER JOIN (
                    SELECT assessment_id, MAX(assessment_date) AS max_date
                    FROM Assessment_Results
                    WHERE user_id = ?
                    GROUP BY assessment_id
                ) AS Latest_Assessments
                ON Assessment_Results.assessment_id = Latest_Assessments.assessment_id 
                    AND Assessment_Results.assessment_date = Latest_Assessments.max_date
                WHERE Assessment_Results.user_id = ?
            ) AS Assessment_Results_Latest 
                ON Assessment_Results_Latest.assessment_id = Assessments.assessment_id
            GROUP BY Competencies.competency_id;""", (user_id,user_id)).fetchall()
    except Exception as e:
        print(f"Error retrieving results: {e}")
        return
    
    if not results:
        print("No results founded for the given user ID.")
        return
    total_score = 0
    number_of_competencies = 0
    data_rows = []
    
    
    for r in results:
        score = r[1]
        name = f'{user[0]} {user[1]}'
        email = user[2]
        competency_name = r[0]
        score = r[1]

        
        total_score += score
        if score > 0:
            number_of_competencies += 1
        data_rows.append([
            name,
            email,
            competency_name,
            score,
            ""
        ])
    name_1 = f'{user[0]}_{user[1]}'
    
    avg = total_score / number_of_competencies
     
    for row in data_rows:
        row[4] = f'{avg:.2}'
   
    try:
        header = ['Name','Email','Competency Name', 'score', 'Average Score']

        csv_file_name = f"competency_report_{name_1}.csv"
        
        with open (csv_file_name, "w") as user_competency:
            wrt = csv.writer(user_competency)

            wrt.writerow(header)
            wrt.writerows(data_rows)
        print(f"\nReport generated and saved as '{csv_file_name}'.")
    except Exception as e:
        print(f"Error writing to CSV file: {e}")
        return

    

def competency_results_summary():
    try:
        connection, cursor = db_connection()
    except Exception as e:
        print(f'Database connection failed:{e}')
    competency_id = safe_input("Please enter Competency ID to generate the report(Type q to return to main menu)")
    if competency_id is None:
        return
    competency_id = competency_id.strip()
    if not competency_id.isdigit():
        print("Invalid input. Competency ID must be a number.")
        return
    try:
        competency = cursor.execute("SELECT name FROM competencies WHERE competency_id = ?", (competency_id,)).fetchone()
        if not competency:
            print("No Competency found with that ID.")
            return
        competency_name = competency[0]
        competency_join_name = '_'.join(competency_name.split(" "))
        
    except Exception as e:
        print(f"Error fetching competency: {e}")
    
    try:
        results = cursor.execute("""SELECT Users.first_name, Users.last_name, COALESCE(Assessment_Results.score, 0), 
        Assessments.name, Assessment_Results.assessment_date
        FROM Users
        LEFT JOIN (
            SELECT Assessment_Results.user_id, Assessment_Results.assessment_id, Assessment_Results.score, Assessment_Results.assessment_date
            FROM Assessment_Results
            INNER JOIN (
                SELECT Assessment_Results.user_id, Assessment_Results.assessment_id, MAX(Assessment_Results.assessment_date) AS latest_date
                FROM Assessment_Results
                GROUP BY Assessment_Results.user_id, Assessment_Results.assessment_id
            ) AS Latest_Assessment
            ON Assessment_Results.user_id = Latest_Assessment.user_id 
                AND Assessment_Results.assessment_id = Latest_Assessment.assessment_id 
                AND Assessment_Results.assessment_date = Latest_Assessment.latest_date
        ) AS Assessment_Results
        ON Assessment_Results.user_id = Users.user_id
        LEFT JOIN Assessments 
            ON Assessments.assessment_id = Assessment_Results.assessment_id
        WHERE Assessments.competency_id = ?
        GROUP BY Users.user_id;""", (competency_id,)).fetchall()
    except Exception as e:
        print(f"Error retriving results: {e}")  
        return 
    print(results)
    if not results:
        print("No results found for the given competency.")
        return
    
    total = 0
    number_of_users = 0
    data_rows = []

    for r in results:
        name = f"{r[0]} {r[1]}"
        score = r[2]
        assessment_name = r[3]
        date_taken = r[4]
        total += score
        if score > 0:
            number_of_users += 1
        data_rows.append([
            competency_name,
            '',
            name,
            score,
            assessment_name,
            date_taken
        ])  
    avg = total / number_of_users
    for row in data_rows:
        row[1] = f'{avg:.2}'
    print(total)
    print(number_of_users)
    try:
        header = ['Competency Name', 'Average Score', 'Name', 'Score','Assessments Name', 'Date Taking']

        csv_file_name = f"competency_report_{competency_join_name}.csv"
        
        with open (csv_file_name, "w") as competency_levels:
            wrt = csv.writer(competency_levels)

            wrt.writerow(header)
            wrt.writerows(data_rows)
        print(f"\nReport generated and saved as '{csv_file_name}'.")
    except Exception as e:
        print(f"Error writing to CSV file: {e}")
        return

      
def import_assessment_results_csv():
    try:
        file_path = safe_input("Please input CSV file name(Type q to return to main menu)")
        if file_path is None:
            return
        file_path = file_path.strip()
        
        connection, cursor = db_connection()
        try:
            csvfile = open(file_path, "r")
        except FileNotFoundError:
            print("File not found. Please check the filename and try again.")
            return
        try:
            with csvfile:
                reader = csv.DictReader(csvfile)
                
                for row in reader:
                    cursor.execute('''
                        INSERT INTO assessment_results (user_id, assessment_id, score, assessment_date, manager_id)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (row['user_id'], row['assessment_id'], row['score'], row['assessment_date'], row['manager_id']))
        except Exception as row_error:
            print(f"Error inserting row{row}:{row_error}")    
        connection.commit()
        
        print("CSV imported successfully.")
    except Exception as e:
        print(f"An error occured: {e}")
        
   

def manager_view():
    while True:
                choice = input("""
                Please select from the options:
                1. View all users
                2. Search for user
                3. Competency Results Summary report
                4. user competency summary report 
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
                """)
                
                if choice == "1": 
                    view_all_users()
                elif choice == "2": 
                    search_user_by_name()
            
                elif choice == "3":
                    competency_results_summary()

                elif choice == "4":
                    user_competency_summary()

                elif choice == "5":
                    list_user_competency_assessments()

                elif choice == "6":
                    
                    loged_in_user.add_user_to_db()

                elif choice == "7":
                    competency.add_competency_to_db()

                elif choice == "8": 
                    assessment.add_assessment_to_competency()

                elif choice == "9":
                    assessment_result.add_assessment_result()

                elif choice == "10":
                    while True:
                        try:
                            
                            user_instance = selecting_user_by_manager()
                            if not user_instance:
                                break
                            user_update = input("""Please select(1 - 7) from the options to edit:\n
                            
                            1.First Name and Last Name
                            2.Phone Number
                            3.Email
                            4.Password
                            5.Role
                            6.Active
                            7.Exit
                            """)
                            
                            if user_update not in ["1", "2", "3","4","5","6","7"]:
                                print("Invalid selection. Please choose from the options")
                                continue
                            if user_update == "1":
                                user_instance.edit_name()
                            elif user_update == "2":
                                user_instance.edit_phone()
                            elif user_update =="3":
                                user_instance.edit_email()
                            elif user_update == "4":
                                user_instance.edit_password()
                            elif user_update == "5":
                                user_instance.edit_role()
                            elif user_update == "6":
                                user_instance.edit_active()
                            elif user_update == "7":
                                print("Goodbye")
                                break     
                        except Exception as e:
                            print(f"Unexpected error: {e}")

                elif choice == "11": 
                    competency.update_competency()

                elif choice == "12":
                    assessment.edit_assessment()

                elif choice == "13":
                    assessment_result.edit_assessment_result()

                elif choice == "14":
                    assessment_result.delete_assessment_result()

                elif choice == "15":
                    import_assessment_results_csv()

                elif choice == "16":
                    print("Goodbye")
                    break

def user_view():         
    while True:
        choice = input("""
        Please select from the options:
        1. View Competency and Assessment Data
        2. Change First Name and Last Name
        3. Change Phone Number
        4. Change Email
        5. Change Password
        6. Log Out
        """)
        if choice not in ["1", "2", "3","4","5","6"]:
            print("Invalid selection. Please choose from the options")
            continue
        if choice == "1": 
            list_user_competency_assessments()
        if choice == "2":  
            loged_in_user.edit_name()
        if choice == "3":
            log_in_result.edit_phone()
        if choice == "4":
            loged_in_user.edit_email()
        if choice == "5":
            loged_in_user.edit_password()
        if choice == "6": 
            print("Goodbye")
            break
    


def selecting_user_by_manager():

    user_id = safe_input("Enter the User ID(Type q to return to main menu):")
    if user_id is None:
        return
    user_id = user_id.strip()
    if not user_id:
        print("User ID can not be empty")
        return   
         
    result = cursor.execute("SELECT user_id, first_name, last_name, phone, email, password, hiring_date, role, active FROM Users WHERE user_id = ? ;",(user_id,)).fetchone()
    
    if not result:
        print("No user found with the provided User ID.")
        return
    user_instance = Users(user_id = result[0],first_name = result[1], last_name = result[2], phone_number = result[3], email = result[4], password = result[5], hiring_date = result[6], role = result[7], active = result[8])
    return user_instance


create_schema()

connection, cursor = db_connection()

while True:
    email_input = input("Please input your email:")
    
    if  email_input:
        loged_in_user = Users(" ", " "," ", " ", " ", " ", " ", " ", " ")  
        competency = Competencies(" ", " ")
        assessment = Assessments(" "," "," ", " ")
        assessment_result = Assessment_results (" ", " "," "," "," ")

        password = input("Please input your password")
        log_in_result = Users.log_in(loged_in_user, email_input, password )

        
        if not log_in_result:  # If login failed
            print("Unable to log in. Please verify your login details.")
            continue

        role =str(log_in_result[1]).lower().strip()
        user_id = log_in_result[0]
            
        if role == "manager":
            manager_view()
            

        if role == "user":
            user_view()
            






    
   
    
    