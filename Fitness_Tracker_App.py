import time
import os
import sqlite3
import datetime
from tabulate import tabulate

# Database connection
connection = sqlite3.connect('sample.db')
cursor = connection.cursor()

# Create Users Table
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(50) UNIQUE,
        password VARCHAR(10),
        age INT,
        gender VARCHAR(10)
        );
    '''
)

cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS workout_plans(
        plan_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        date TEXT,
        activity VARCHAR(20),
        FOREIGN KEY (user_id) REFERENCES Users (user_id)
        )
    '''
)

# Create workout_details Table
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS workout_details(
        workout_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        date TEXT,
        activity VARCHAR(20),
        calories_burned REAL,
        FOREIGN KEY (user_id) REFERENCES Users (user_id)
        )
    '''
)

# Create goal table
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS goal_settings(
        goal_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        activity VARCHAR(20),
        duration_in_mins INT,
        weight_to_loss REAL,
        FOREIGN KEY (user_id) REFERENCES Users(user_id)
    )
    '''
)

def insert_goal_settings(user_id, activity, duration_in_mins, weight_to_loss):
    cursor.execute(
        '''
        INSERT INTO goal_settings(user_id, activity, duration_in_mins, weight_to_loss)
        VALUES (?, ?, ?, ?)
        ''',
        (user_id, activity, duration_in_mins, weight_to_loss)
    )
    connection.commit()

def insert_users(name, password, age, gender):
    cursor.execute(
        '''
        INSERT INTO Users(name, password, age, gender)
        VALUES (?, ?, ?, ?)
        ''',
        (name, password, age, gender)
    )
    connection.commit()

def insert_workout_plans(user_id, date, activity):
    cursor.execute(
        '''
        INSERT INTO workout_plans (user_id, date, activity)
        VALUES (?, ?, ?)
        ''',
        (user_id, date, activity)
    )
    connection.commit()

def insert_workout_details(user_id, date, activity, calories_burned):
    cursor.execute(
        '''
        INSERT INTO workout_details(user_id, date, activity, calories_burned)
        VALUES (?, ?, ?, ?)
        ''',
        (user_id, date, activity, calories_burned)
    )
    connection.commit()

class User:
    @staticmethod
    def authentication():
        print("Enter the following details\n")
        try:
            name = input("Enter the username: ")
            password = input("Enter the password: ")
            user_query = cursor.execute(
                'SELECT * FROM Users WHERE name = ?', (name,)
            ).fetchone()

            if user_query:
                print('Username already exists. Please log in.')
                User.login_verification(name, password)
                return

            age = int(input("Enter your age: "))
            if age < 18 or age > 60:
                print("Sorry, this platform is not suitable for you!!")
                return

            gender = input("Enter your gender: ")
            insert_users(name, password, age, gender)
            print("Registered Successfully!!")
            time.sleep(0.7)
            print("Good to go")

        except ValueError:
            print("Please enter a valid input")
            return

    @staticmethod
    def login_verification(name=None, password=None):
        if name is None or password is None:
            name = input("Enter the username: ")
            password = input("Enter the password: ")

        user_query = cursor.execute(
            'SELECT * FROM Users WHERE name = ? AND password = ?', (name, password)
        ).fetchone()

        if user_query:
            print("Logged in successfully")
            time.sleep(0.5)
            os.system('cls')
            return user_query[0]  # Return user_id
        else:
            print("Invalid username or password! Please try again.")
            return None

class FitnessTracker(User):
    @staticmethod
    def activity_tracking(user_id):
        os.system('cls')
        activity = {1: 'Running', 2: 'Swimming', 3: 'Cycling'}
        for i, j in activity.items():
            print(f"{i}. {j}")
        try:
            select = int(input("Select your fitness activity: "))
            choice = activity.get(select, 'Invalid Choice')
            if choice == 'Invalid Choice':
                print(choice)
                return
        except ValueError:
            print("Please enter a valid number!")
            return

        weight = float(input("Enter your weight: "))
        input("Can we start? (s) ")
        start_time = time.time()

        print(f"{choice}...")
        input("Do you want to stop? (e) ")
        end_time = time.time()

        diff_time = (end_time - start_time) / 60

        if select == 1:
            calories_burned = 9 * diff_time * weight
        elif select == 2:
            calories_burned = 8 * diff_time * weight
        else:
            calories_burned = 7 * diff_time * weight

        date = datetime.datetime.today().strftime('%Y-%m-%d')
        calories_burned = round(calories_burned,2)
        insert_workout_details(user_id, date, choice, calories_burned)
        print(f"You burned {calories_burned:.2f} calories")

    @staticmethod
    def workout_plans():
        os.system('cls')
        activity = {1: 'Running', 2: 'Swimming', 3: 'Cycling'}
        for i, j in activity.items():
            print(f"{i}. {j}")
        try:
            select = int(input("Select your fitness activity: "))
            choice = activity.get(select, 'Invalid Choice')
            if choice != 'Invalid Choice':
                if select == 1:
                    print('''Weekly Schedule
Monday: Speed Intervals – 30 mins (Sprint & jog cycles)
Tuesday: Tempo Run – 45 mins (Maintain steady, challenging pace)
Wednesday: Hill Training – 40 mins (Run uphill, jog down)
Thursday: Recovery Jog – 30 mins (Light and slow)
Friday: Fartlek Training – 45 mins (Random pace changes)
Saturday: Long Run – 60-90 mins (Improve endurance)
Sunday: Rest or Stretching''')
                elif select == 2:
                    print('''Weekly Schedule
Monday: Freestyle Endurance – 1000m (Continuous swim)
Tuesday: Sprint Training – 50m x 10 reps (High-speed intervals)
Wednesday: Technique & Drills – 45 mins (Focus on stroke efficiency)
Thursday: Open Water or Long Swim – 1500m+
Friday: Mixed Stroke Training – 60 mins (Freestyle, Backstroke, Breaststroke)
Saturday: Endurance & Speed – 2000m (Combination of long & fast swims)
Sunday: Active Recovery – 30 mins (Slow & relaxed swim)
''')
                else:
                    print('''Weekly Schedule
Monday: Interval Training – 30-45 mins (Alternate between high & low intensity)
Tuesday: Endurance Ride – 60 mins (Maintain steady pace)
Wednesday: Hill Training – 40 mins (Focus on climbs)
Thursday: Recovery Ride – 30 mins (Low-intensity, easy pace)
Friday: Speed Work – 45 mins (Sprints & cadence drills)
Saturday: Long Ride – 90+ mins (Build stamina)
Sunday: Rest or Light Stretching
''')
            else:
                print('Invalid choice')
        except ValueError:
            print("Please enter a valid input")

    @staticmethod
    def custom_plans(user_id):
        os.system('cls')
        print('Create Your own custom Plans:\n')
        activity = {1: 'Running', 2: 'Swimming', 3: 'Cycling'}
        for i, j in activity.items():
            print(f"{i}. {j}")
        try:
            select = int(input("Select your fitness activity: "))
            choice = activity.get(select, 'Invalid Choice')
            if choice == 'Invalid Choice':
                print('Invalid choice')
                return

            date = input('Enter date (YYYY-MM-DD): ')
            insert_workout_plans(user_id, date, choice)
            print("Workout plan added successfully!")
        except ValueError:
            print("Please enter a valid input")

    @staticmethod
    def goal_setting(user_id):
        os.system('cls')
        print("Set your goal")

        activity = {1: 'Running', 2: 'Swimming', 3: 'Cycling'}
        for i, j in activity.items():
            print(f"{i}. {j}")
        try:
            type_of_activity = int(input("Enter your activity type: "))
            weight_to_loss = float(input("Enter the weight to loss: "))
            choice = activity.get(type_of_activity, 'Invalid Choice')
            if choice == 'Invalid Choice':
                print('Invalid choice')
                return

            time_to_cover = float(input("Enter the Duration: "))
            insert_goal_settings(user_id, choice, time_to_cover, weight_to_loss)
            print('Goal settings set')
        except ValueError:
            print("Please enter a valid input")

def main():
    user = input("Login or Sign Up: ").strip().lower()
    if user == 'login':
        print("----LOGIN----")
        user_id = User.login_verification()
        if user_id is None:
            return
    elif user == 'sign up':
        print("----SIGN UP----")
        User.authentication()
        os.system('cls')
        print('Please Login Again')
        user_id = User.login_verification()
        if user_id is None:
            return
    else:
        print("Invalid Choice")
        return

    check = True
    while check:
        os.system('cls')
        print('Select your fitness activity:')
        assist = {1: 'Start workout', 2: 'Workout Plans', 3: 'Custom Work Plans', 4: 'Set Goal',5:'Leader Board'}
        for i, j in assist.items():
            print(f"{i}. {j}")
        try:
            input_choice = int(input("Enter your choice: "))
            choice = assist.get(input_choice, 'Invalid Choice')
            if choice == 'Invalid Choice':
                print("Please enter a valid input")
                continue

            if input_choice == 1:
                FitnessTracker.activity_tracking(user_id)
            elif input_choice == 2:
                FitnessTracker.workout_plans()
            elif input_choice == 3:
                FitnessTracker.custom_plans(user_id)
            elif input_choice == 4:
                FitnessTracker.goal_setting(user_id)
            elif input_choice == 5:
                result = cursor.execute('''
                select Users.* , workout_details.calories_burned
                from Users
                join workout_details 
                on workout_details.user_id = Users.user_id
                order by workout_details.calories_burned desc
                ''').fetchall()

                column_name = [result[0] for result in cursor.description]

                if result:
                    print(tabulate(result, headers=column_name))
                else:
                    print('currently learder board is empty')
        except ValueError:
            print("Please enter a valid input")

        yes_no = input("Do you want to continue? (y/n): ").strip().lower()
        if yes_no != 'y':
            check = False

    connection.close()

if __name__ == '__main__':
    main()