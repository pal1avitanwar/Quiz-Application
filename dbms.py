import mysql.connector
import random


conn = mysql.connector.connect(
    host="localhost",  # Replace with your MySQL server address
    user="root",       # Replace with your MySQL username
    password="PS17@PPSSSS",  # Replace with your MySQL password
    database="quiz_app"
)
cursor = conn.cursor()


def register():
    username = input("Enter a username: ")
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        print("User already exists!")
        return False

    password = input("Enter a password: ")
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    conn.commit()
    print("Registration successful!")
    return True


def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    if cursor.fetchone():
        print("Login successful!")
        return username
    print("Invalid username or password!")
    return None


def quiz(subject, user):
    print(f"\nStarting {subject} quiz!")
    cursor.execute("SELECT * FROM questions WHERE subject = %s", (subject,))
    questions = cursor.fetchall()

    if not questions:
        print("No questions available for this subject.")
        return

    selected_questions = random.sample(questions, min(5, len(questions)))
    score = 0

    for i, q in enumerate(selected_questions, 1):
        print(f"\nQ{i}: {q[2]}")  
        options = [q[3], q[4], q[5], q[6]]  
        for idx, option in enumerate(options, 1):
            print(f"{idx}. {option}")

        while True:
            try:
                ans = int(input("Your answer (1/2/3/4): "))
                if 1 <= ans <= 4:
                    break
                print("Invalid option. Please choose between 1 and 4.")
            except ValueError:
                print("Please enter a valid number.")

        if options[ans - 1] == q[7]:  
            print("Correct!")
            score += 1
        else:
            print(f"Wrong! The correct answer was: {q[7]}")

    print(f"\n{user}, your score is {score}/5.")


def main():
    print("Welcome to the Quiz Application!")
    user = None

    while not user:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            if register():
                continue
        elif choice == "2":
            user = login()
        elif choice == "3":
            print("Goodbye!")
            conn.close()
            return
        else:
            print("Invalid choice!")

    while True:
        print("\nSubjects:\n1. C++\n2. Python\n3. DSA")
        choice = input("Choose a subject (1-3): ")
        if choice == "1":
            quiz("C++", user)
        elif choice == "2":
            quiz("Python", user)
        elif choice == "3":
            quiz("DSA", user)
        else:
            print("Invalid choice!")
            continue

        play_again = input("Do you want to take another quiz? (yes/no): ").lower()
        if play_again != "yes":
            print("Goodbye!")
            conn.close()
            break

if __name__ == "__main__":
    main()
