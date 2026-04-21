from academic_system import AcademicSystem
from student import Student
from faculty import Faculty


def faculty_menu(system, faculty):
    while True:
        print("\n╔══════════════════════════════╗")
        print("║     FACULTY MENU             ║")
        print("╠══════════════════════════════╣")
        print("║ 1. View Dashboard            ║")
        print("║ 2. Add Student               ║")
        print("║ 3. Remove Student            ║")
        print("║ 4. List Students             ║")
        print("║ 5. Search Student            ║")
        print("║ 6. Add Course                ║")
        print("║ 7. List Courses              ║")
        print("║ 8. Enrol Student in Course   ║")
        print("║ 9. Record Marks              ║")
        print("║ 10. Record Attendance        ║")
        print("║ 11. View Student Report      ║")
        print("║ 12. Save & Exit              ║")
        print("╚══════════════════════════════╝")

        choice = input("Enter choice: ").strip()

        try:
            if choice == "1":
                faculty.show_dashboard()

            elif choice == "2":
                sid = input("Student ID: ").strip()
                name = input("Name: ").strip()
                pwd = input("Password: ").strip()
                course = input("Programme (e.g. M.Sc. AI & ML): ").strip()
                system.add_student(sid, name, pwd, course)

            elif choice == "3":
                sid = input("Student ID to remove: ").strip()
                system.remove_student(sid)

            elif choice == "4":
                system.list_students()

            elif choice == "5":
                kw = input("Search by name or ID: ").strip()
                system.search_student(kw)

            elif choice == "6":
                cid = input("Course ID (e.g. CS401): ").strip()
                name = input("Course Name: ").strip()
                credits = int(input("Credits: ").strip())
                system.add_course(cid, name, credits, faculty.person_id)

            elif choice == "7":
                system.list_courses()

            elif choice == "8":
                sid = input("Student ID: ").strip()
                cid = input("Course ID: ").strip()
                student = system.get_student(sid)
                faculty.enrol_student(student, cid)

            elif choice == "9":
                sid = input("Student ID: ").strip()
                cid = input("Course ID: ").strip()
                score = float(input("Score (0-100): ").strip())
                student = system.get_student(sid)
                faculty.add_marks(student, cid, score)

            elif choice == "10":
                sid = input("Student ID: ").strip()
                cid = input("Course ID: ").strip()
                pct = float(input("Attendance % (0-100): ").strip())
                student = system.get_student(sid)
                faculty.mark_attendance(student, cid, pct)

            elif choice == "11":
                sid = input("Student ID: ").strip()
                student = system.get_student(sid)
                student.generate_report()

            elif choice == "12":
                system.save_data()
                print("Goodbye!")
                break

            else:
                print("Invalid choice. Please try again.")

        except ValueError as e:
            print(f"Error: {e}")


def student_menu(system, student):
    while True:
        print("\n╔══════════════════════════════╗")
        print("║     STUDENT MENU             ║")
        print("╠══════════════════════════════╣")
        print("║ 1. View Dashboard            ║")
        print("║ 2. View Available Courses    ║")
        print("║ 3. View My Marks & Grades    ║")
        print("║ 4. View My Attendance        ║")
        print("║ 5. Generate Performance Rpt  ║")
        print("║ 6. Save & Exit               ║")
        print("╚══════════════════════════════╝")

        choice = input("Enter choice: ").strip()

        try:
            if choice == "1":
                student.show_dashboard()

            elif choice == "2":
                system.list_courses()

            elif choice == "3":
                marks = student.marks
                if not marks:
                    print("No marks recorded yet.")
                else:
                    print(f"\n  {'Course':<12} {'Score':>6} {'Grade':>6}")
                    print("  " + "-" * 28)
                    for cid, score in marks.items():
                        print(f"  {cid:<12} {score:>6} {student.compute_grade(cid):>6}")

            elif choice == "4":
                att = student.attendance
                if not att:
                    print("No attendance data yet.")
                else:
                    print(f"\n  {'Course':<12} {'Attendance':>12} {'Status'}")
                    print("  " + "-" * 36)
                    for cid, pct in att.items():
                        status = "OK" if pct >= 75 else "⚠ LOW"
                        print(f"  {cid:<12} {pct:>10.1f}%   {status}")

            elif choice == "5":
                student.generate_report()

            elif choice == "6":
                system.save_data()
                print("Goodbye!")
                break

            else:
                print("Invalid choice. Please try again.")

        except ValueError as e:
            print(f"Error: {e}")


def seed_demo_data(system):
    """Add sample data so the app is usable out of the box."""
    try:
        system.add_faculty("F01", "Mr. Akshay Awasthi", "faculty123", "Computer Science (AI & ML)")
        system.add_student("S01", "Aditya Bharadwaj", "student123", "M.Sc. AI & ML")
        system.add_course("CS401", "Machine Learning", 4, "F01")
        system.add_course("CS402", "Data Structures", 3, "F01")
        system.add_course("CS403", "Python Programming", 3, "F01")
        fac = system.get_faculty("F01")
        stu = system.get_student("S01")
        fac.enrol_student(stu, "CS401")
        fac.enrol_student(stu, "CS402")
        fac.enrol_student(stu, "CS403")
        system.save_data()
        print("\n[Demo data loaded. Use IDs above to log in.]")
    except ValueError:
        pass  # already seeded


def main():
    print("\n" + "=" * 50)
    print("   STUDENTTRACK — Student Record Management")
    print("        Chandigarh University | 2026")
    print("=" * 50)

    system = AcademicSystem()

    import os
    if not os.path.exists("students.pkl"):
        seed_demo_data(system)

    print("\nDefault demo credentials:")
    print("  Faculty  → ID: F01  | Password: faculty123")
    print("  Student  → ID: S01  | Password: student123")

    for _ in range(3):
        print("\n-- Login --")
        user_id = input("User ID  : ").strip()
        password = input("Password : ").strip()
        user = system.login(user_id, password)

        if user is None:
            print("Invalid credentials. Try again.")
            continue

        print(f"\nWelcome, {user.name}!")
        from faculty import Faculty
        from student import Student
        if isinstance(user, Faculty):
            faculty_menu(system, user)
        else:
            student_menu(system, user)
        break
    else:
        print("Too many failed attempts. Exiting.")


if __name__ == "__main__":
    main()