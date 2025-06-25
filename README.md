📌 Face Recognition Attendance System
https://img.shields.io/badge/Python-3.8%252B-blue
https://img.shields.io/badge/OpenCV-4.5%252B-orange
https://img.shields.io/badge/face__recognition-1.3%252B-red
A secure, automated attendance system using face recognition with anti-spoofing (liveness detection) and GUI support.

🚀 Features
Real-time face recognition with dlib/face_recognition.

Liveness detection to prevent spoofing (see liveness.py).

GUI interface (gui.py) for user-friendly interactions.

Database integration (database.py) for storing attendance records.

Modular design: Separate scripts for registration (register.py), reports (reports.py), and utilities (utils.py).

Pre-trained model: Uses shape_predictor_68_face_landmarks.dat for accurate facial landmarks.

📂 Project Structure
plaintext
.
├── data/                  # Stores registered face encodings/images
├── attendance_reports/    # Generated attendance logs (CSV/Excel)
├── src/                   # Core source files
│   ├── attendance.py      # Main attendance logic
│   ├── auth.py            # Authentication utilities
│   ├── database.py        # Database operations
│   ├── gui.py             # Graphical user interface
│   ├── liveness.py        # Anti-spoofing checks
│   ├── register.py        # New user registration
│   └── utils.py           # Helper functions
├── requirements.txt       # Dependencies
└── shape_predictor_68_face_landmarks.dat  # dlib landmark model
🛠 Installation
Clone the repo:

bash
git clone https://github.com/your-username/face-attendance-system.git
cd face-attendance-system
Install dependencies:

bash
pip install -r requirements.txt
(Example requirements.txt):

text
opencv-python
face-recognition
dlib
numpy
pandas
tkinter
Download the pre-trained model:

Ensure shape_predictor_68_face_landmarks.dat is placed in the root folder.

🖥 Usage
1. Register New Users
bash
python src/register.py
Captures face images and stores encodings in data/.

2. Run Attendance System
bash
python src/attendance.py
Real-time face detection + liveness check.

Logs attendance to attendance_reports/.

3. Generate Reports
bash
python src/reports.py
Exports attendance data to CSV/Excel.

4. Launch GUI (Optional)
bash
python src/gui.py
📷 Demo
https://demo_gui.png (Replace with your actual screenshot)

🤝 Contributing
Bug fixes: Open an issue or submit a PR.

Enhancements:

Add cloud sync (Firebase/AWS).

Improve liveness detection (liveness.py).

Extend GUI features (gui.py).
