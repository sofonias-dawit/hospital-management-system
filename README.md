
# 🏥 HealthEase - A Comprehensive Hospital Management System

A full-stack, enterprise-grade Hospital Management System (HMS) designed to streamline hospital operations. Built with a robust Django REST Framework backend and a dynamic React.js frontend, this application provides a complete, role-based solution for managing patients, staff, and hospital workflows.

## ✨ Key Features

- **Role-Based Access Control**: Secure, distinct dashboards and functionalities for all major roles:
  - **Admin**: Manages users, departments, and views system-wide analytics.
  - **Doctor**: Manages appointments, views assigned patients, updates medical records, and writes prescriptions.
  - **Patient**: Books appointments, views personal medical history (records & prescriptions), and uses an AI Symptom Checker.
  - **Receptionist**: Manages all appointments across the hospital and handles patient billing.
  - **Nurse**: Manages ward and bed assignments, including admitting and discharging patients.
- **Interactive UI**: A clean, responsive interface built with React and Tailwind CSS, featuring a persistent sidebar for easy navigation.
- **Dynamic Data Management**: Live search, interactive modals for creating/editing data, and real-time updates without page reloads.
- **AI Integration**: A built-in Symptom Checker that uses a machine learning model to predict potential conditions based on user input.
- **Secure Authentication**: Backend API protected by JSON Web Tokens (JWT) for secure communication.
- **Full CRUD Functionality**: Administrators have complete Create, Read, Update, and Delete capabilities for users and departments directly from the UI.

## 🛠️ Tech Stack

- **Backend**:
  - Python 3.11+
  - Django & Django REST Framework
  - MySQL (Database)
  - `djangorestframework-simplejwt` (for JWT Authentication)
- **Frontend**:
  - React.js 18+
  - React Router
  - Axios (for API calls)
  - Tailwind CSS (for styling)
  - Recharts (for analytics charts)
  - Heroicons (for UI icons)
- **AI Module**:
  - Scikit-learn
  - Pandas & NumPy
- **Deployment (Optional)**:
  - Docker & Docker Compose

---

## 🚀 Getting Started

Follow these instructions to set up and run the project on your local machine.

### Prerequisites

- Python 3.9+ and Pip
- Node.js and npm
- A running MySQL Server (you can use the MySQL from a package like WAMP/XAMPP)

### 1. Backend Setup (Django)

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/sofonias-dawit/hospital-management-system.git
    cd your-repo-name
    ```

2.  **Navigate to the Backend & Create Virtual Environment**
    ```bash
    cd backend
    python -m venv venv
    venv\Scripts\activate  # On Windows
    # source venv/bin/activate  # On macOS/Linux
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
    *Note: If `requirements.txt` does not exist, generate it with `pip freeze > requirements.txt`.*

4.  **Set Up the Database**
    - Ensure your MySQL server is running.
    - Create a new database named `HospitalDB`: `CREATE DATABASE HospitalDB;`

5.  **Configure Environment Variables**
    - In the `backend` directory, create a file named `.env`.
    - Copy the contents from `backend/.env.example` (if it exists) or use the template below.
    - **Fill in your actual database credentials.**
    ```env
    SECRET_KEY='a-very-strong-and-secret-key-that-you-generate'
    DEBUG=True
    DB_NAME='HospitalDB'
    DB_USER='your_mysql_user'      # e.g., 'root' for WAMP
    DB_PASSWORD='your_mysql_password'  # e.g., leave empty for WAMP
    DB_HOST='127.0.0.1'
    DB_PORT='3306'
    ```

6.  **Run Database Migrations**
    ```bash
    python manage.py migrate
    ```

7.  **Create Your Administrator Account**
    This command will prompt you to create your own username and password for the admin dashboard.
    ```bash
    python manage.py createsuperuser
    ```

8.  **Run the Backend Server**
    ```bash
    python manage.py runserver
    ```
    The backend will now be running at `http://127.0.0.1:8000`. Keep this terminal open.

### 2. Frontend Setup (React)

1.  **Open a new terminal**.
2.  **Navigate to the Frontend Directory**
    ```bash
    cd frontend
    ```

3.  **Install Dependencies**
    ```bash
    npm install
    ```

4.  **Run the Frontend Server**
    ```bash
    npm start
    ```
    The application will automatically open in your browser at `http://localhost:3000`.

### 3. AI Model Setup

The project comes with a pre-trained AI model. If you want to retrain it:
1.  Navigate to the `ai-module` directory: `cd ../ai-module`.
2.  Install dependencies: `pip install scikit-learn pandas numpy`.
3.  Run the training script: `python train_model.py`.
4.  Manually copy the newly generated `.joblib` files into the `backend/ml_models/` directory.