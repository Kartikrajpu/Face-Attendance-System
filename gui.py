import PySimpleGUI as sg
from database import get_subjects, init_database, add_subject
from register import register_student
from attendance import mark_attendance
from reports import generate_report

# Initialize database
init_database()

def show_admin_gui():
    layout = [
        [sg.TabGroup([
            [sg.Tab("Register Student", [
                [sg.Text("Roll No:"), sg.Input(key="-ROLL-")],
                [sg.Text("Name:"), sg.Input(key="-NAME-")],
                [sg.Button("Register Face", key="-REGISTER-")]
            ]),
            sg.Tab("Add Subject", [
                [sg.Text("Subject Name:"), sg.Input(key="-SUBJECT-")],
                [sg.Button("Add Subject", key="-ADD_SUBJECT-")]
            ])]
        ])],
        [sg.Button("Exit", key="-EXIT-")]
    ]
    
    window = sg.Window("Admin Panel", layout)
    
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "-EXIT-"):
            break
        elif event == "-REGISTER-":
            if values["-ROLL-"] and values["-NAME-"]:
                register_student(values["-ROLL-"], values["-NAME-"])
            else:
                sg.popup_error("Please enter both roll number and name!")
        elif event == "-ADD_SUBJECT-":
            if values["-SUBJECT-"]:
                add_subject(values["-SUBJECT-"])
                sg.popup(f"Subject '{values['-SUBJECT-']}' added successfully!")
            else:
                sg.popup_error("Please enter a subject name!")
    
    window.close()

def show_teacher_gui():
    subjects = get_subjects()
    subject_names = [s['name'] for s in subjects]
    
    layout = [
        [sg.Text("Select Subject:"), sg.Combo(subject_names, key="-SUBJECT-")],
        [sg.Button("Start Attendance", key="-ATTENDANCE-")],
        [sg.Button("Generate Report", key="-REPORT-")],
        [sg.Button("Exit", key="-EXIT-")]
    ]
    
    window = sg.Window("Teacher Panel", layout)
    
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "-EXIT-"):
            break
        elif event == "-ATTENDANCE-":
            if values["-SUBJECT-"]:
                mark_attendance(values["-SUBJECT-"])
            else:
                sg.popup_error("Please select a subject first!")
        elif event == "-REPORT-":
            if values["-SUBJECT-"]:
                generate_report(values["-SUBJECT-"])
            else:
                sg.popup_error("Please select a subject first!")
    
    window.close()

if __name__ == "__main__":
    show_admin_gui()  # or show_teacher_gui() for testing