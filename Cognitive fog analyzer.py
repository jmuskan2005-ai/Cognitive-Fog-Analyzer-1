import csv
import datetime
import os
import statistics

# This function stores each entry in a CSV file.
# A new file is created automatically the first time you run the program.
def save_log(record):
    file_name = "cognitive_fog_log.csv"
    new_file = not os.path.isfile(file_name)

    with open(file_name, "a", newline="") as f:
        writer = csv.writer(f)

        if new_file:
            writer.writerow([
                "Date", "Sleep Hours", "Focus Level",
                "Stress Level", "Screen Time (hrs)",
                "Fog Score"
            ])

        writer.writerow(record)


# This function calculates the cognitive fog score using a simple weighted model.
# Lower sleep, high stress, low focus, and high screen time increase the fog score.
def calculate_fog_score(sleep, focus, stress, screen):
    score = (
        (10 - focus) * 0.35 +
        stress * 0.40 +
        (screen / 2) * 0.15 +
        (7 - sleep) * 0.10
    )
    # Score is kept within a 0–10 range
    return round(max(0, min(score, 10)), 2)


# This function reads the CSV file and shows basic statistics.
# Useful for tracking your emotional and cognitive patterns over time.
def show_summary():
    file_name = "cognitive_fog_log.csv"

    if not os.path.isfile(file_name):
        print("\nNo previous data found. Start by entering a record.")
        return

    scores = []

    with open(file_name, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            scores.append(float(row["Fog Score"]))

    print("\nSummary of your cognitive fog history:")
    print(f"Total entries: {len(scores)}")
    print(f"Average fog score: {round(statistics.mean(scores), 2)}")
    print(f"Highest fog score: {max(scores)}")
    print(f"Lowest fog score: {min(scores)}")
    print()


# The main program loop handles user choices and input.
def main():
    print("\nWelcome to the Cognitive Fog Analyzer (Terminal Edition)")

    while True:
        print("\nWhat would you like to do?")
        print("1. Add a new entry")
        print("2. View summary")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            try:
                sleep = float(input("How many hours did you sleep? "))
                focus = int(input("Rate your focus today (1–10): "))
                stress = int(input("Rate your stress level (1–10): "))
                screen = float(input("How many hours of screen time today? "))
            except ValueError:
                print("Please enter valid numbers. Let's try again.")
                continue

            fog_score = calculate_fog_score(sleep, focus, stress, screen)

            record = [
                datetime.date.today(),
                sleep, focus, stress, screen, fog_score
            ]

            save_log(record)

            print(f"\nYour cognitive fog score today is: {fog_score}/10")

            if fog_score >= 7:
                print("You seem mentally overloaded. Consider resting a bit.")
            elif fog_score >= 4:
                print("Your fog level is moderate. Small breaks may help.")
            else:
                print("Your fog level is low. You're functioning well!")

        elif choice == "2":
            show_summary()

        elif choice == "3":
            print("Thank you for using the Cognitive Fog Analyzer. Take care!")
            break

        else:
            print("That option isn't recognized. Please try again.")


if __name__ == "__main__":
    main()