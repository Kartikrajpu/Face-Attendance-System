from auth import login
from gui import show_admin_gui, show_teacher_gui

if __name__ == "__main__":
    user_role = login()
    if user_role == "admin":
        show_admin_gui()
    elif user_role == "teacher":
        show_teacher_gui()
    else:
        print("Access denied!")