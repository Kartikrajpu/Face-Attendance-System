import dlib
import cv2
import face_recognition
from database import add_student
from liveness import detect_blink

def register_student(roll_no, name):
    # Initialize face detection
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    
    cap = None
    try:
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Use DirectShow for Windows
        if not cap.isOpened():
            print("Error: Could not open camera")
            return False

        registered = False
        last_blink_time = 0
        blink_cooldown = 1.0  # 1 second cooldown between blink detections

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to capture frame")
                break

            # Mirror the frame
            frame = cv2.flip(frame, 1)
            
            # Display instructions
            cv2.putText(frame, "Press 'S' to Scan | 'Q' to Quit", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            
            current_time = cv2.getTickCount() / cv2.getTickFrequency()
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("Registration cancelled by user")
                break
                
            if key == ord('s') and not registered:
                if current_time - last_blink_time > blink_cooldown:
                    if detect_blink(frame, predictor, detector):
                        last_blink_time = current_time
                        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        face_encodings = face_recognition.face_encodings(rgb_frame)
                        
                        if face_encodings:
                            add_student(roll_no, name, face_encodings[0])
                            registered = True
                            cv2.putText(frame, "REGISTERED!", (50, 100),
                                       cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
                            cv2.imshow("Registration", frame)
                            cv2.waitKey(2000)  # Show success for 2 seconds
                            break

            cv2.imshow("Registration", frame)

    except Exception as e:
        print(f"Error during registration: {str(e)}")
        return False
        
    finally:
        # Always release resources
        if cap is not None:
            cap.release()
        cv2.destroyAllWindows()
        
    return registered