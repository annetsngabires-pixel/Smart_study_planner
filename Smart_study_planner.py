import csv
import os

FILE_NAME = "study_log.txt"


def classify_session(duration):
    """Classify a study session based on its duration."""
    if duration < 30:
        return "Short"
    elif duration <= 90:
        return "Medium"
    else:
        return "Long"


def add_session(sessions):
    """Prompt the user for session details and add the session."""
    print("\n--- Add Study Session ---")

    subject = input("Enter subject: ").strip()
    topic = input("Enter topic covered: ").strip()
    date = input("Enter date/day label: ").strip()

    # Keep asking until the user enters a positive number.
    while True:
        duration_input = input("Enter duration in minutes: ").strip()

        try:
            duration = float(duration_input)

            if duration <= 0:
                print("Duration must be a positive number.")
            else:
                break

        except ValueError:
            print("Invalid duration. Please enter a number.")

    session = {
        "subject": subject,
        "topic": topic,
        "date": date,
        "duration": duration
    }

    sessions.append(session)
    print("Study session added successfully!")


def print_session_header():
    """Print the header used for session tables."""
    print("-" * 90)
    print(
        f"{'Subject':<20}"
        f"{'Topic':<25}"
        f"{'Date':<15}"
        f"{'Duration':<12}"
        f"{'Class':<10}"
    )
    print("-" * 90)


def print_session(session):
    """Display one session in a formatted row."""
    classification = classify_session(session["duration"])

    duration_text = f"{session['duration']:.1f} min"

    print(
        f"{session['subject']:<20}"
        f"{session['topic']:<25}"
        f"{session['date']:<15}"
        f"{duration_text:<12}"
        f"{classification:<10}"
    )


def view_sessions(sessions):
    """Display all logged study sessions."""
    print("\n--- All Study Sessions ---")

    if not sessions:
        print("No study sessions have been recorded yet.")
        return

    print_session_header()

    for session in sessions:
        print_session(session)

    print("-" * 90)


def search_by_subject(sessions, subject):
    """Display sessions matching a subject, ignoring letter case."""
    search_subject = subject.strip().lower()

    matching_sessions = [
        session for session in sessions
        if session["subject"].strip().lower() == search_subject
    ]

    if not matching_sessions:
        print(f"\nNo sessions found for subject: {subject}")
        return

    print(f"\n--- Sessions for {subject} ---")
    print_session_header()

    total_time = 0

    for session in matching_sessions:
        print_session(session)
        total_time += session["duration"]

    print("-" * 90)
    print(f"Total time spent on {subject}: {total_time:.1f} minutes")
    print(f"Total time in hours: {total_time / 60:.2f} hours")


def search_menu(sessions):
    """Ask the user for a subject and perform a search."""
    subject = input("\nEnter subject to search for: ").strip()

    if not subject:
        print("Subject cannot be empty.")
        return

    search_by_subject(sessions, subject)


def study_statistics(sessions):
    """Calculate and display study statistics."""
    print("\n--- Study Statistics ---")

    if not sessions:
        print("No study sessions available for statistics.")
        return

    total_minutes = sum(session["duration"] for session in sessions)

    print(f"Total hours studied overall: {total_minutes / 60:.2f} hours")

    # Calculate total study time for each subject.
    subject_totals = {}

    for session in sessions:
        subject = session["subject"]

        if subject not in subject_totals:
            subject_totals[subject] = 0

        subject_totals[subject] += session["duration"]

    print("\nTotal hours studied per subject:")

    for subject, minutes in subject_totals.items():
        print(f"- {subject}: {minutes / 60:.2f} hours")

    # The subject with the smallest total study time is the weakest area.
    weakest_subject = min(subject_totals, key=subject_totals.get)

    print(
        f"\nWeakest area (least study time): "
        f"{weakest_subject} "
        f"({subject_totals[weakest_subject] / 60:.2f} hours)"
    )

    # Find the single longest study session.
    longest_session = max(sessions, key=lambda session: session["duration"])

    print("\nSingle longest study session:")
    print(f"Subject: {longest_session['subject']}")
    print(f"Topic: {longest_session['topic']}")
    print(f"Date: {longest_session['date']}")
    print(f"Duration: {longest_session['duration']:.1f} minutes")
    print(f"Classification: {classify_session(longest_session['duration'])}")


def save_sessions(sessions):
    """Save all study sessions to study_log.txt."""
    try:
        with open(FILE_NAME, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            # Header row makes the saved file easier to understand.
            writer.writerow(["Subject", "Topic", "Date", "Duration"])

            for session in sessions:
                writer.writerow([
                    session["subject"],
                    session["topic"],
                    session["date"],
                    session["duration"]
                ])

        print(f"\nSessions saved successfully to {FILE_NAME}.")

    except OSError as error:
        print(f"Error saving sessions: {error}")


def load_sessions():
    """Load existing study sessions from study_log.txt."""
    sessions = []

    if not os.path.exists(FILE_NAME):
        # This is the first run, so there is no saved data yet.
        return sessions

    try:
        with open(FILE_NAME, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                try:
                    session = {
                        "subject": row["Subject"],
                        "topic": row["Topic"],
                        "date": row["Date"],
                        "duration": float(row["Duration"])
                    }

                    # Only load valid positive durations.
                    if session["duration"] > 0:
                        sessions.append(session)

                except (ValueError, KeyError):
                    # Ignore incorrectly formatted rows rather than crashing.
                    continue

    except OSError as error:
        print(f"Error loading sessions: {error}")

    return sessions


def display_menu():
    """Display the main menu."""
    print("\n" + "=" * 45)
    print("       SMART STUDY PLANNER")
    print("=" * 45)
    print("1. Add a study session")
    print("2. View all sessions")
    print("3. Search sessions by subject")
    print("4. View statistics")
    print("5. Save and exit")
    print("=" * 45)


def main():
    """Main program loop."""
    sessions = load_sessions()

    print("Welcome to the Smart Study Planner!")

    if sessions:
        print(f"{len(sessions)} saved session(s) loaded.")
    else:
        print("No previous sessions found. Starting with an empty log.")

    while True:
        display_menu()

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_session(sessions)

        elif choice == "2":
            view_sessions(sessions)

        elif choice == "3":
            search_menu(sessions)

        elif choice == "4":
            study_statistics(sessions)

        elif choice == "5":
            save_sessions(sessions)
            print("Thank you for using Smart Study Planner. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
