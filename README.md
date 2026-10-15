# 🚗 Parking Management System

A web-based **Parking Management System** developed using Python and Flask to simplify parking operations. The system provides user authentication, parking slot booking, vehicle check-in and check-out, and parking report management through a user-friendly interface.

## 📌 Project Overview

Managing parking spaces manually can be time-consuming and difficult. This project provides a web-based solution to manage parking activities efficiently, maintain parking records, and simplify the booking process.

## ✨ Features

- 🔐 **User Authentication** — User registration and login.
- 🅿️ **Parking Management** — Manage parking-related operations.
- 🚘 **Parking Booking** — Book parking spaces through the web interface.
- 📥 **Vehicle Check-In** — Record vehicle entry details.
- 📤 **Vehicle Check-Out** — Process vehicle exits.
- 📊 **Reports** — View parking-related reports.
- 🎨 **Interactive Interface** — HTML, CSS, JavaScript, images, and animations.
- 🗄️ **Database Integration** — Store and manage application data using SQLite.

## 🛠️ Technologies Used

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite
- **Tools:** Visual Studio Code, Git, GitHub

## 📂 Project Structure

```text
parkingmanagementsystem/
│
├── app.py
├── main_ui.py
├── parking.py
├── init_db.py
├── config.py
├── requirements.txt
├── README.md
│
├── database/
├── static/
│   ├── css/
│   ├── images/
│   ├── js/
│   └── videos/
│
└── templates/
    ├── index.html
    ├── login.html
    ├── signup.html
    ├── checkin.html
    ├── checkout.html
    ├── report.html
    └── permission.html
```

*Note: The actual files and folders may vary slightly depending on the project version.*

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/sneeehalshewale-afk/parkingmanagementsystem.git
```

### 2. Navigate to the Project Directory

```bash
cd parkingmanagementsystem
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

**Windows:**

```cmd
venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Initialize the Database

If required by the project setup, run:

```bash
python init_db.py
```

### 7. Run the Application

```bash
python app.py
```

### 8. Open in Your Browser

Visit:

http://127.0.0.1:5000

## 💻 Requirements

- Python 3.10 or a compatible Python version
- pip package manager
- A modern web browser
- Required Python dependencies listed in `requirements.txt`

## 🔒 Security and Data

Do not publish passwords, secret keys, real user records, or private parking information in the repository. Use sample data for demonstrations and configure sensitive values securely.

## 🚀 Future Enhancements

- Real-time parking slot availability
- Online payment integration
- QR-code-based parking entry and exit
- Admin dashboard and advanced analytics
- Email or SMS booking notifications
- Mobile-friendly responsive interface

## 🎯 Project Objective

The main objective is to develop a simple and efficient digital parking management solution that reduces manual work, organizes parking records, and improves the user experience.

## 👨‍💻 Author

**Snehal Shewale**

GitHub: [@sneeehalshewale-afk](https://github.com/sneeehalshewale-afk)

## 📄 License

No license has been specified yet. All rights are reserved by the author unless a license is added to this repository.

