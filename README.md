# Expense Management System

A simple yet powerful expense management system featuring a Streamlit frontend and a FastAPI backend. Track your expenses efficiently with interactive analytics and a user-friendly interface.

## Project Structure

- **frontend/**: Streamlit application code for the user interface.
- **backend/**: FastAPI backend server code powering the API.
- **tests/**: Automated test cases for frontend and backend components.
- **requirements.txt**: Python dependencies for the project.
- **README.md**: Project overview and setup instructions.

## Features
- Add, update, and delete expense records
- Filter and analyze expenses by category and payment method.
- Monthly trend visualizations and detailed breakdowns.
- Responsive UI with interactive charts powered by Streamlit.

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/expense-management-system.git
   cd expense-management-system
   ```
1. **Install dependencies:**:   
   ```commandline
    pip install -r requirements.txt
   ```
1. **Run the FastAPI server:**:   
   ```commandline
    uvicorn server.server:app --reload
   ```
1. **Run the Streamlit app:**:   
   ```commandline
    streamlit run frontend/app.py

## Contributing
Contributions are more than welcome! Feel free to open issues or submit pull requests.
