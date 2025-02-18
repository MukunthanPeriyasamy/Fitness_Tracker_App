import time
import os
import sqlite3
import datetime

connection = sqlite3.connect('sample.db')
cursor = connection.cursor()

# Create Users Table
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS Users(
        name VARCHAR(50),
        password TEXT
    );
    '''
)

cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS workout_plans(
        Monday VARCHAR(50),
        Tuesday VARCHAR(50),
        Wednesday VARCHAR(50),
        Thursday VARCHAR(50),
        Friday VARCHAR(50),
        Saturday VARCHAR(50),
        Sunday VARCHAR(50)
    );
    '''
)

# Create workout_details Table
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS workout_details(
        day DATE,
        activity VARCHAR(10),
        calories_burned REAL
    );
    '''
)

# Create user_details Table
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS User_details(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        password TEXT NOT NULL,
        age INTEGER,
        weight REAL,
        gender VARCHAR(10)
    );
    '''
)

# Create goal table
cursor.execute(
    '''
    create table if not exists goal_settings(
    activity VARCHAR(10),
    weight_to_loss real,
    time_to_cover real
    )
    '''
)

def insert_goal_settings(activity, weight_to_loss, time_to_cover):
    cursor.execute(
        '''
        insert into goal_settings(activity, weight_to_loss, time_to_cover) values (?, ?, ?)
        ''',
        (activity, weight_to_loss, time_to_cover)
    )

# Insert Users
def insert_users(name, password):
    cursor.execute(
        '''
        INSERT INTO Users VALUES (?, ?)
        ''',
        (name, password)
    )
    connection.commit()

# Insert User Details
def user_details(password, age, weight, gender):
    cursor.execute(
        '''
        INSERT INTO User_details (password, age, weight, gender) VALUES (?,?, ?, ?)
        ''',
        (password, age, weight, gender)
    )
    connection.commit()

# Insert workout plans
def insert_workout_plans(monday, tuesday, wednesday, thursday, friday, saturday, sunday):
    cursor.execute(
        '''
        INSERT INTO workout_plans (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''',
        (monday, tuesday, wednesday, thursday, friday, saturday, sunday)
    )
    connection.commit()


class User:

    @staticmethod
    def authentication(password):
        print("Enter the following details\n")
        try:
            age = int(input("Enter your age: "))
            if age < 18 or age > 60:
                print("Sorry, this platform is suitable for you!!")
                User.authentication(password)

            weight = float(input("Enter your weight: "))
            gender = input("Enter your gender: ")
        except ValueError:
            print("Please enter a valid input")
            return

        user_details(password, age, weight, gender)
        print("Registered Successfully!!")
        time.sleep(0.7)
        print("Good to go")
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def login_verification(name, password):
        user_query = cursor.execute(
            'SELECT * FROM Users WHERE name = ? AND password = ?', (name, password)
        ).fetchone()

        if user_query:
            print("Logged in successfully")
            time.sleep(0.5)
            os.system('cls')
        else:
            print("Invalid username or password! Please try again.")
            return

class FitnessTracker(User):

    @staticmethod
    def activity_tracking(password):
        os.system('cls')
        activity = {1: 'Running', 2: 'Swimming', 3: 'Cycling'}
        for i, j in activity.items():
            print(f"{i}. {j}")
        try:
            select = int(input("Select your fitness activity: "))
            choice = activity.get(select, 'Invalid Choice')
            if choice != 'Invalid Choice':
                print(f'You Have Selected: {choice}')
            else:
                print(choice)
                return
        except ValueError:
            print("Please enter a valid number!")
            return

        weight = cursor.execute(
            'SELECT weight FROM User_details WHERE password= ?', (password,)
        ).fetchone()

        if weight:
            weight = weight[0]

        input("Can we start? (s) ")
        start_time = time.time()

        print(f"{activity[select]}...")
        input("Do you want to stop? (e) ")
        end_time = time.time()

        diff_time = (end_time - start_time) / 60

        if select == 1:
            calories = 9 * diff_time * weight
        elif select == 2:
            calories = 8 * diff_time * weight
        else:
            calories = 7 * diff_time * weight

        date = datetime.datetime.today().strftime('%d-%m-%Y')

        cursor.execute(
            '''INSERT INTO workout_details VALUES (?, ?, ?)''',
            (date, choice, calories)
        )
        connection.commit()

        print(f"You burned {calories:.2f} calories")

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
    def custom_plans(password):
        os.system('cls')
        print('Create Your own custom Plans:\n')
        activity = {1: 'Running', 2: 'Swimming', 3: 'Cycling'}
        for i, j in activity.items():
            print(f"{i}. {j}")
        select = int(input("Select your fitness activity: "))
        choice = activity.get(select, 'Invalid Choice')
        if choice != 'Invalid Choice':
            if select == 1:
                print(f'Create Plan for {choice}')
            elif select == 2:
                print(f'Create Plan for {choice}')
            else:
                print(f'Create Plan for {choice}')
            Monday = input('Monday: ')
            Tuesday = input('Tuesday: ')
            Wednesday = input('Wednesday: ')
            Thursday = input('Thursday: ')
            Friday = input('Friday: ')
            Saturday = input('Saturday: ')
            Sunday = input('Sunday: ')
        else:
            print('Invalid choice')
            return
        # Now, inserting the workout plan without the password
        insert_workout_plans(Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday)

    @staticmethod
    def goal_setting():
        os.system('cls')
        print("Set your goal")

        activity = {1: 'Running', 2: 'Swimming', 3: 'Cycling'}
        for i, j in activity.items():
            print(f"{i}. {j}")
        type_of_activity = int(input("Enter your activity type: "))
        weight_to_loss = float(input("Enter the weight to loss: "))
        choice = activity.get(type_of_activity, 'Invalid Choice')
        if choice != 'Invalid Choice':
                time_to_cover  = float(input("Enter the Duration: "))
                insert_goal_settings(choice,weight_to_loss, time_to_cover)
                print('Goal settings set')
        else:
            print('Invalid choice')
            return

def main():
    user = input("Login or Sign Up: ").strip().lower()
    if user == 'login':
        print("----LOGIN----")
        name = input("Enter the username: ")
        password = input("Enter the password: ")
        User.login_verification(name, password)

    elif user == 'sign up':
        print("----SIGN UP----")
        name = input("Enter the username: ")
        password = input("Enter the password: ")
        insert_users(name, password)
        print("Registered Successfully!!")
        User.authentication(password)
        time.sleep(0.7)
    else:
        print("Invalid Choice")
        return

    check = True
    while check:
        os.system('cls')
        assist = {1: 'Start workout', 2: 'Workout Plans', 3: 'Custom Work Plans',4:'Set Goal'}
        for i, j in assist.items():
            print(f"{i}. {j}")
        input_choice = int(input("Enter your choice: "))
        choice = assist.get(input_choice, 'Invalid Choice')
        if choice != 'Invalid Choice':
            if input_choice == 1:
                FitnessTracker.activity_tracking(password)
            elif input_choice == 2:
                FitnessTracker.workout_plans()
            elif input_choice == 3:
                FitnessTracker.custom_plans(password)
            elif input_choice == 4:
                FitnessTracker.goal_setting()

        else:
            print("Please enter a valid input")

        yes_no = input("Do you want to continue? (y/n): ").strip().lower()
        if yes_no != 'y':
            check = False

    connection.close()

if __name__ == '__main__':
    main()
