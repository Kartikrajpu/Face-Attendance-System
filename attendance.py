import cv2
import face_recognition
import numpy as np
from database import get_students, log_attendance, get_subject_id
import time

def mark_attendance(subject_name):
    # Get subject ID with type safety
    subject_id = get_subject_id(subject_name)
    if subject_id is None:
        print(f"Error: Subject '{subject_name}' not found")
        return False
    
    # Ensure proper type conversion
    try:
        if hasattr(subject_id, 'item'):
            subject_id = subject_id.item()
        subject_id = int(subject_id)
    except Exception as e:
        print(f"Error converting subject ID: {e}")
        return False
    
    # Rest of your attendance marking code...

    known_students = get_students()
    if not known_students:
        print("Error: No registered students found")
        return False

    # Prepare face data
    known_encodings = []
    known_rolls = []
    for roll, data in known_students.items():
        if data['encoding'] is not None:
            known_encodings.append(data['encoding'])
            known_rolls.append(roll)

    # Initialize camera
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("Error: Could not open camera")
        return False

    last_logged = {}
    cooldown = 30  # seconds

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to capture frame")
                break

            frame = cv2.flip(frame, 1)
            rgb_frame = frame[:, :, ::-1]

            # Face detection
            face_locs = face_recognition.face_locations(rgb_frame)
            face_encs = face_recognition.face_encodings(rgb_frame, face_locs)

            current_time = time.time()
            for (top, right, bottom, left), face_enc in zip(face_locs, face_encs):
                matches = face_recognition.compare_faces(known_encodings, face_enc)
                if True in matches:
                    best_match = np.argmin(face_recognition.face_distance(known_encodings, face_enc))
                    roll_no = known_rolls[best_match]

                    if (roll_no not in last_logged or 
                        current_time - last_logged[roll_no] > cooldown):
                        try:
                            log_attendance(roll_no, subject_id)
                            last_logged[roll_no] = current_time
                            print(f"Logged attendance for {roll_no}")
                        except Exception as e:
                            print(f"Database error: {e}")

            # Display
            cv2.putText(frame, f"Subject: {subject_name}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            cv2.putText(frame, "Press Q to quit", (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            cv2.imshow('Attendance', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        cap.release()
        cv2.destroyAllWindows()
        time.sleep(0.5)

    return True