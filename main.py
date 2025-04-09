

import sqlite3
import bcrypt
from datetime import datetime
import csv

def db_connection():
    connection = sqlite3.connect("competency.db")
    cursor = connection.cursor()
    return connection, cursor

def create_schema():
    connection, cursor = db_connection() 
    with open ('tables.txt', 'r') as my_table:
        read_tables = my_table.read()
        cursor.executescript(read_tables)     
    connection.commit()



create_schema()

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
        
        result = cursor.execute("SELECT password, role , active FROM Users WHERE email = ? ;" , (email,)).fetchone()
        if result is None:
            print("User not found.")
            return False
        saved_password = result[0]
        role = result[1]
        active = result[2]
        if active == 0:
            print("Your access has been denied.")
            return

        if isinstance(saved_password, str):
            saved_password = saved_password.encode('utf-8') # Encode if it's a string / Ensure it's in bytes
        
        if bcrypt.checkpw(password.encode('utf-8'), saved_password): # Check if the password matches
            print("User founded")
            return role.lower()
        
        else:
            print("Incorrect password.")
            return False
    
    def edit_user(self):
       
        while True:
            user_update = input("""Please select(1 - 6) from the options to edit:\n
                        
                        1.First Name and Last Name\n
                        2.Phone Number\n
                        3.Email\n
                        4.password\n
                        5.role
                        6.Active
                        7.Exit
                        """)
            if user_update == "1": #tested / good 
                self.first_name = input("Enter new first name: ")
                self.last_name = input("Enter new last name: ")
                connection, cursor = db_connection()
                cursor.execute("UPDATE Users SET first_name = ?,last_name =? WHERE user_id = ?;", (self.first_name,self.last_name,self.user_id))
                connection.commit()
            
            if user_update == "2":#tested / good
                self.phone = input("Please input new phone number")
                connection, cursor = db_connection()
                cursor.execute("UPDATE Users SET phone = ? WHERE user_id = ?;", (self.phone, self.user_id))
                connection.commit()
                print("Phone number updated successfully.")

                
            if user_update == "3":#tested / good
                self.email = input("Please input new email")
                connection, cursor = db_connection()
                cursor.execute("UPDATE Users SET email = ? WHERE user_id = ?;", (self.email, self.user_id))
                connection.commit()
                print("Email updated successfully.")

                    
            if user_update == "4":#tested / good
                password = input("Please input new password")
                self.password = self.hash_password(password)
                connection, cursor = db_connection()
                cursor.execute("UPDATE Users SET password = ? WHERE user_id = ?;", (self.password, self.user_id))
                connection.commit()
                print("Password updated successfully.")

            if user_update == "5":
                self.role = input("Please input new role")
                connection, cursor = db_connection()
                cursor.execute("UPDATE Users SET role = ? WHERE user_id = ?;", (self.role, self.user_id))
                connection.commit()                
                print("Role updated successfully.")
    
            if user_update == "6": 
                self.active = input("Please input (1 for active) or (0 for deactive) user").strip()
                connection, cursor = db_connection()
                cursor.execute("UPDATE Users SET active = ? WHERE user_id = ?;", (self.active, self.user_id))
                connection.commit()
                print("Active updated successfully.")

                 
            if user_update =="7":
                print("Return to main menu")
                break
        

    def add_user_to_db(self):
        print("\n=== Add New User ===")

        self.first_name = input("please input First Name").capitalize()
        self.last_name = input("please input Last Name").capitalize()
        self.phone_number = input("please input phone number")
        self.email = input("please input Email")
        self.date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        password = input ("please input password here")
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.hiring_date = input("please input hiring date")
        self.role = input("please input role").capitalize()
        self.active = input("please input 1 or 0 ")
        
        connection, cursor = db_connection()
        
        query = """INSERT INTO Users(first_name, last_name, phone, email, date_created, password, hiring_date, role, active) VALUES (
        ?, ?, ?, ?, ?, ?, ?, ?, ?);""" 
        values = (self.first_name, self.last_name, self.phone_number, self.email, self.date_created, self.password.decode('utf-8'), self.hiring_date, self.role, self.active)

        cursor.execute(query, values) 
        connection.commit()
        print("User saved successfully!")


def view_all_users ():
    connection, cursor = db_connection()

    results = cursor.execute("SELECT * FROM Users;").fetchall()
    print(f" {"User_id":<10} {"First Name":<12} {"Last Name":<15} {"Phone Number":<15} {"Email":<20} {"Date Created":<15} {"Hiring Date":<15} {"Role":<10} {"Active":<7}")
    for row in results:
        print(f" {row[0]:<10} {row[1]:<12} {row[2]:<15} {row[3]:<15} {row[4]:20} {row[5]:<15} {row[7]:<15} {row[8]:<10} {row[9]:<7}")


def search_user_by_name():
    connection, cursor = db_connection()
    user_id_input = input("Please input name to search").strip()

    results = cursor.execute("SELECT * FROM Users WHERE first_name LIKE ? OR last_name LIKE ?", (f'%{user_id_input}%', f'%{user_id_input}%')).fetchall()
    if not results:
        print("No matches found.")
        return
    if results:
        print("\nMatching users:")
        print(f" {"User_id":<10} {"First Name":<12} {"Last Name":<15} {"Phone Number":<15} {"Email":<20} {"Date Created":<15} {"Hiring Date":<15} {"Role":<10} {"Active":<7}")
        
    
        for row in results:
            print(f" {row[0]:<10} {row[1]:<12} {row[2]:<15} {row[3]:<15} {row[4]:20} {row[5]:<15} {row[7]:<15} {row[8]:<10} {row[9]:<7}")
        
            
            
             

def search_user_by_user_id():
    connection, cursor = db_connection()
    view_all_users()
    user_id_input = input("Please input user_id").strip()

    if not user_id_input.isdigit():
        print("Invalid user_id. Please enter a numeric ID.")
        return
    if int(user_id_input):
       
        result = cursor.execute("SELECT * FROM Users WHERE user_id = ?", (user_id_input,)).fetchone()
        
        
        if result:
            print(f"""
            User_id: {result[0]}
            First Name: {result[1]}
            Last Name: {result[2]}
            Phone Number: {result[3]}
            Email: {result[4]}
            Date Created: {result[5]}
            Hiring Date: {result[7]}
            Role : {result[8]}
            Active: {result[9]}
            """)
            
            return result 

        else:
            print("User not found.")
            return



        
    

class Competencies:
    def __init__(self, competency_id, name):
        self.competency_id = competency_id
        self.name = name
        self.date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    
    def add_competency_to_db(self):
        print("\n=== Add Competency ===")

        self.name = input ("Please input competency name")
        
        
        connection, cursor = db_connection()
        
        query = """INSERT INTO Competencies(name, date_created) VALUES (
        ?, ?);""" 
        values = (self.name, self.date_created)

        cursor.execute(query, values) 
        connection.commit()
        print("Competency saved successfully!")

    # def list_competencies(self):
    #     connection, cursor = db_connection()
        
    #     competencies = cursor.execute("SELECT * FROM competencies").fetchall()
        
    #     print("\n=== Competencies ===")
    #     for c in competencies:
    #         print(f"{c[0]} - {c[1]} (Created: {c[2]})")


    def update_competency(self,competency_id, name):
        if self.competency_id is None:
            print("Error: Competency ID is not set.")
            return
        self.name = name
        self.competency_id = competency_id
        try:
            connection, cursor = db_connection()
            cursor.execute("UPDATE Competencies SET name = ? WHERE competency_id = ?;", (self.name, self.competency_id))
            
            connection.commit()
            
            print("Competency updated successfully.")
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
        self.competency_id = input ("Please enter the Competency ID to add an assessment.")
        self.name = input ("Please enter the assessment name")
        self.assessment_type = input ("Please enter assessment type")

        connection, cursor = db_connection()
        
        query = """INSERT INTO Assessments(competency_id,name, assessment_type, date_created) VALUES (
        ?, ?,?,?);""" 
        values = (self.competency_id, self.name, self.assessment_type, self.date_created)

        cursor.execute(query, values) 
        connection.commit()
        print("Assessment saved successfully!")


    def edit_assessment(self):
        self.assessment_id = input("Please enter Assessment ID to edit")
        assessment_update = input ("""Please select from list(1 - 3)
                                   1.Update Competency ID
                                   2.Update Assessment Name
                                   3.Update Assessment Type """)
        if assessment_update == "1":
            self.competency_id = input ("Please enter new Competency ID to add an assessment.")
            connection, cursor = db_connection()
            cursor.execute("UPDATE Assessments SET competency_id = ? WHERE assessment_id = ?;", (self.competency_id, self.assessment_id))
            connection.commit()
            print("Competency_id updated successfully.")
        if assessment_update == "2":
            self.name = input ("Please enter new assessment name")
            connection, cursor = db_connection()
            cursor.execute("UPDATE Assessments SET name = ? WHERE assessment_id = ?;", (self.name, self.assessment_id))
            connection.commit()
            print("Assessment Name updated successfully.")
        if assessment_update == "3":
            self.assessment_type = input ("Please enter new assessment type")
            connection, cursor = db_connection()
            cursor.execute("UPDATE Assessments SET assessment_type = ? WHERE assessment_id = ?;", (self.assessment_type, self.assessment_id))
            connection.commit()
            print("Assessment Type updated successfully.")


# def list_user_assessments():
#     connection, cursor = db_connection()
#     user_id = input("please input user_id")
#     results =cursor.execute("""SELECT Assessment_Results.result_id, Competencies.name, Assessments.name, Assessment_Results.score ,Assessments.date_created
#     FROM Assessments JOIN Assessment_Results
#     ON Assessments.assessment_id = Assessment_Results.assessment_id
#     WHERE Assessment_Results.user_id = ?; """, (user_id,)).fetchall()

#     print(f"\nAssessment Results for User {user_id}:")
#     print(f'{"Result ID":<10} {"Assessment Name":<35} {"Result Score":<10} {"Assessment Date Created":<12}')
#     for r in results:
#         print(f"{r[0]:<10} {r[1]:<30} {r[2]:<10} {r[3]:<12}")

def list_user_competency_assessments():
    connection, cursor = db_connection()
    user_id = input("please input user_id")
    results =cursor.execute("""SELECT Assessment_Results.result_id, Competencies.name, Assessments.name, Assessment_Results.score ,Assessments.date_created
    FROM Competencies JOIN Assessments
    ON Competencies.competency_id = Assessments.competency_id
    JOIN Assessment_Results
    ON Assessments.assessment_id = Assessment_Results.assessment_id
    WHERE Assessment_Results.user_id = ?; """, (user_id,)).fetchall()

    print(f"\nAssessment Results for User {user_id}:")
    print(f'{"Result ID":<10} {"Competency Name":<20} {"Assessment Name":<35} {"Result Score":<10} {"Assessment Date Created":<12}')
    for r in results:
        print(f"{r[0]:<10} {r[1]:<20} {r[2]:<35} {r[3]:<10} {r[4]:<12}")
    




class Assessment_results:
    def __init__(self,user_id, assessment_id, score,assessment_date, manager_id):
        self.user_id = user_id
        self.assessment_id = assessment_id
        self.score = score
        self.assessment_date = assessment_date
        self.manager_id = manager_id

    def add_assessment_result (self):
        self.user_id = input ("Please enter the User ID")
        self.assessment_id = input ("Please enter the Assessment ID ")
        self.score = int(input ("Please enter user's Score(0 - 4)"))
        self.assessment_date = input("Date Taken (YYYY-MM-DD): ")
        self.manager_id = input ("Please enter Manager ID (who administered): ")

        connection, cursor = db_connection()
        query = ("INSERT INTO Assessment_Results(user_id, assessment_id, score, assessment_date, manager_id)VALUES(?, ?, ?, ?,?)")
        values = (self.user_id, self.assessment_id, self.score, self.assessment_date, self.manager_id)
        cursor.execute(query, values)
        connection.commit()
        print("Assessment Result saved successfully!")

    def edit_assessment_result(self):
        connection, cursor = db_connection()
        self.result_id = input("Please enter Result ID to edit")
        result_update = input ("""Please select from list(1 - 4)
                                   1.Update User ID
                                   2.Update Assessment ID
                                   3.Update Score
                                   4.Update Manager ID """)
        if result_update == "1":
            self.user_id = input ("Please enter new User ID")
            cursor.execute("UPDATE Assessment_Results SET user_id = ? WHERE result_id = ?;", (self.user_id, self.result_id))
            connection.commit()
            print("User ID updated successfully.")

        if result_update == "2":
            self.assessment_id = input ("Please enter new Assessment ID")
            cursor.execute("UPDATE Assessment_Results SET assessment_id = ? WHERE result_id = ?;", (self.assessment_id, self.result_id))
            connection.commit()
            print("Assessment ID updated successfully.")

        if result_update == "3":
            self.score = input ("Please enter new Score")
            cursor.execute("UPDATE Assessment_Results SET score = ? WHERE result_id = ?;", (self.score, self.result_id))
            connection.commit()
            print("Score updated successfully.")

        if result_update == "4":
            self.manager_id = input ("Please enter new Manager ID")
            cursor.execute("UPDATE Assessment_Results SET manager_id = ? WHERE result_id = ?;", (self.manager_id, self.result_id))
            connection.commit()
            print("Manager ID updated successfully.")

    
    def delete_assessment_result(self):
        connection, cursor = db_connection()
        self.result_id = input("Select result_id to delete")
        cursor.execute("""DELETE FROM Assessment_results WHERE result_id = ? ;""",(self.result_id,))   
        connection.commit()
        print(f"Result ID {self.result_id} has been removed successfully.")


    
def user_competency_summary():# work on getting last score, here i get the max score, last score not always the max
    connection, cursor = db_connection()
    user_id = input("Please enter  User ID to generate the report")
    user = cursor.execute("SELECT first_name, last_name, email FROM users WHERE user_id = ?", (user_id,)).fetchone()
    print(f"\n=== Competency Summary for {user[0]} {user[1]} ({user[2]}) ===")
    results = cursor.execute("""
        SELECT Competencies.name, COALESCE(Assessment_Results.score, 0)
        FROM Competencies
        LEFT JOIN Assessments
            ON Assessments.competency_id = Competencies.competency_id
        LEFT JOIN Assessment_Results 
            ON Assessment_Results.assessment_id = Assessments.assessment_id
        WHERE Assessment_Results.assessment_date = (
            SELECT MAX(assessment_date)
            FROM Assessment_Results
            WHERE Assessment_Results.user_id =?
        )
        AND Assessment_Results.user_id = ?
        GROUP BY Competencies.competency_id;""", (user_id, user_id)).fetchall()

    total_score = 0
    data_rows = []
    competencies_query =cursor.execute("SELECT name FROM Competencies;").fetchall()
    competencies_len = len(competencies_query)

    print(competencies_len)
    print(f'{"Competency Name":<20} {"Score"}\n')

    for r in results:
        score = r[1]
        name = f'{user[0]} {user[1]}'
        email = user[2]
        competency_name = r[0]
        score = r[1]

        print(f"{r[0]:<20}: {r[1]}")
        total_score += score
        data_rows.append([
            name,
            email,
            competency_name,
            score,
            ""
        ])


    if results:
        avg = total_score / competencies_len
        print(f"\nAverage Score: {round(avg, 2)}")
    else:
        avg = 0

    for row in data_rows:
        row[4] = avg

    
    if results:
        header = ['Name','Email','Competency Name', 'score', 'Average Score']

        csv_file_name = f"competency_report_{name}.csv"
        # with open ("competency_levels.csv", "w") as competency_levels:
        with open (csv_file_name, "w") as user_competency:
            wrt = csv.writer(user_competency)

            wrt.writerow(header)
            wrt.writerows(data_rows)
        print(f"\nReport generated and saved as '{csv_file_name}'.")
    else:
        print("No results found for the given competency.")

    




def competency_results_summary():
    connection, cursor = db_connection()
    competency_id = input("Please enter Competency ID to generate the report")
    competency = cursor.execute("SELECT name FROM competencies WHERE competency_id = ?", (competency_id,)).fetchone()
    competency_name = competency[0]
    print(f"\n=== Competency Summary: {competency_name} ===\n")

    
    results = cursor.execute("""
        SELECT Users.first_name, Users.last_name, COALESCE(Assessment_Results.score, 0),Assessments.name, Assessment_Results.assessment_date
        FROM Users 
        LEFT JOIN Assessment_Results 
            ON Assessment_Results.user_id = Users.user_id
        LEFT JOIN Assessments 
            ON Assessments.assessment_id = Assessment_Results.assessment_id
        WHERE Assessment_Results.assessment_date = (
            SELECT MAX(assessment_date)
            FROM Assessment_Results
            WHERE Assessment_Results.user_id = Users.user_id
        )

        AND Assessments.competency_id = ?

        GROUP BY Users.user_id;""", (competency_id,)).fetchall()
    

    users = results[0]
    total = 0
    data_rows = []
    print(f'{"Name":<20} {"Score":<6} {"Assessment Name":<30} {"Last Taken":<20}\n')
    for r in results:
        name = f"{r[0]} {r[1]}"
        score = r[2]
        assessment_name = r[3]
        date_taken = r[4]
        print(f"{name:<20} {r[2]:<6} {r[3]:<30} {r[4]:<20})")
        total += score
        data_rows.append([
            competency_name,
            '',
            name,
            score,
            assessment_name,
            date_taken
        ])

    if results:
        avg = total / len(users)
        print(f"\nAverage Score: {round(avg, 2)}")
    else:
        avg = 0

    for row in data_rows:
        row[1] = avg

    
    if results:
        header = ['Competency Name', 'Average Score', 'Name', 'Score','Assessments Name', 'Date Taking']

        csv_file_name = f"competency_report_{competency_name}.csv"
        # with open ("competency_levels.csv", "w") as competency_levels:
        with open (csv_file_name, "w") as competency_levels:
            wrt = csv.writer(competency_levels)

            wrt.writerow(header)
            wrt.writerows(data_rows)
        print(f"\nReport generated and saved as '{csv_file_name}'.")
    else:
        print("No results found for the given competency.")

    
def import_assessment_results_csv():
    file_path = input("Please input CSV file name")
    connection, cursor = db_connection()

    with open(file_path, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursor.execute('''
                INSERT INTO assessment_results (user_id, assessment_id, score, assessment_date, manager_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (row['user_id'], row['assessment_id'], row['score'], row['assessment_date'], row['manager_id']))
    connection.commit()
    
    print("CSV imported successfully.")
    

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
        exit()

    role =str(log_in_result).lower().strip()
    print(role)
        
    if role == "manager":
        while True:
            manager_need = input("""please select from the options\n
                            1.view all users\n
                            2.search for user \n
                            3.view a report of all users and their competency levels for a given competency\n
                            4.view a competency level report for a user\n
                            5.view a list of assessments for a user\n
                            6.Adding User\n
                            7.add a new competency\n
                            8.add a new assessment to a competency\n
                            9.add an assessment result for a user for an assessment (this is like recording test results for a user)\n
                            10.edit a user's information\n
                            11.edit a competency\n 
                            12.edit an assessment\n
                            13.edit an assessment result\n
                            14.delete an assessment result\n
                            15.import_assessment_results_csv\n
                            16.Log out """)
            
            if manager_need == "1": #tested / done
                view_all_users()
            if manager_need == "2": #tested / done 
                search_method = input("""Please select your search method
                            1.Search by Name
                            2.Search by User ID""")
                if search_method == "1": 
                    search_user_by_name()
                if search_method == "2":
                    search_user_by_user_id()
        
            if manager_need == "3":
                competency_results_summary()

            if manager_need == "4":
                user_competency_summary()

            if manager_need == "5":#tested / done
                list_user_competency_assessments()

            if manager_need == "6":#tested / done
                
                loged_in_user.add_user_to_db()

            if manager_need == "7":#tested / done
                competency.add_competency_to_db()

            if manager_need == "8":#tested / done 
                assessment.add_assessment_to_competency()

            if manager_need == "9":#tested / done
                assessment_result.add_assessment_result()

            if manager_need == "10":#tested / done

                user_id = input("Enter the User ID of the employee you wish to edit:")
    
                result = cursor.execute("SELECT user_id, first_name, last_name, phone, email, password, hiring_date, role, active FROM Users WHERE user_id = ? ;",(user_id)).fetchone()
        
                user_instance = Users(user_id = result[0],first_name = result[1], last_name = result[2], phone_number = result[3], email = result[4], password = result[5], hiring_date = result[6], role = result[7], active = result[8])

                user_instance.edit_user()

            if manager_need == "11": #tested / done 
                competency_id_input = input ("Please input Competency ID to edit")
                if competency_id_input:
                    competency_name = input ("Please input the Competency Name")
                    competency.update_competency(competency_id_input,competency_name)

            if manager_need == "12":#tested / done
                assessment.edit_assessment()

            if manager_need == "13":#tested / done
                assessment_result.edit_assessment_result()

            if manager_need == "14":#tested / done
                assessment_result.delete_assessment_result()

            if manager_need == "15":
                import_assessment_results_csv()

            if manager_need == "16":
                print("Goodbye")
                break



    if role != "manager":
        while True:
            user_need = input("""Please select(1 - 5) from the options:\n
                            1.Competency and Assessment data\n
                            2.Changing First Name and Last Name\n
                            3.Changing Phone Number\n
                            4.Changing Email\n
                            5.Changing password\n
                            6. Log Out
                            """)
            if user_need == "1": #tested / done
                list_user_competency_assessments()
            if user_need == "2": #tested / done 
                first_name = input ("Please input your First Name")
                last_name = input ("Please input your Last Name")    
                loged_in_user.update_name(first_name, last_name)

            if user_need == "3":#tested / done
                phone = input("Please input your new phone number")
                loged_in_user.update_phone(phone)

            if user_need == "4":#tested / done
                email = input("Please input your new email")
                loged_in_user.update_email(email)

            if user_need == "5":#tested / done
                password = input("Please input your new password")
                loged_in_user.update_password(password)

            if user_need == "6": #tested / done
                print("Goodbye")
                break








        




    
   
    
    