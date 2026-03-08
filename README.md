# Army Amenities Portal

A minimal viable product (MVP) web application for managing army personnel amenities and supplies requests.

## Features

- **User Registration & Login** – Army personnel register with army number, name, position, email, and phone
- **Demand Submission** – Users submit requests for specific items with quantities
- **Store IC Dashboard** – Inventory controller reviews all pending demands and updates status (Accept, Reject, Delay)
- **Demand Tracking** – Users view their demand history with status updates
- **Real-time Status Badges** – Visual indicators for demand status (Pending, Accepted, Rejected, Delayed)

## Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: MySQL
- **Frontend**: HTML, Bootstrap 5, Jinja2 Templates
- **Icons**: Bootstrap Icons

## Project Structure

```
├── main.py                 # FastAPI application & routes
├── database.py            # MySQL database operations
├── requirements.txt       # Python dependencies
├── templates/
│   ├── base.html          # Base template with navbar & footer
│   ├── home.html          # Home page
│   ├── login.html         # User login
│   ├── register.html      # User registration
│   ├── user_dashboard.html        # User demand submission & history
│   └── store_ic_dashboard.html    # Store IC demand management
└── README.md
```

## Setup & Installation

### Prerequisites
- Python 3.8+
- MySQL Server
- Virtual environment (venv)

### Steps

1. **Clone/Extract the project**
   ```bash
   cd army_amenities_project
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # macOS/Linux
   # or
   .venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup MySQL Database**
   - Ensure MySQL is running
   - Database and tables will be created automatically on first run
   - Default connection: `localhost`, user: `root`, password: `password`
   - *(Update credentials in database.py if needed)*

5. **Run the application**
   ```bash
   uvicorn main:app --port 8000
   ```

6. **Access the application**
   - Open browser and go to `http://localhost:8000`

## Usage

### User Flow
1. Register with an 8-character army number
2. Login with army number and password
3. Submit demands for items (select from predefined list)
4. View demand history and status

### Store IC Flow
1. Login with Store IC credentials (Username: `store_ic`, Password: `admin123`)
2. View all pending demands in dashboard
3. Click action buttons to Accept, Delay, or Reject demands

## Item List

Available items for demand:
- Boots (Aku, Altberg, Iturri)
- MTP Clothing (Shirt, Jacket Smock, Trousers, Goretex Top/Bottom)
- Accessories (Socks, Olive T-shirt, Jungle Hat, Fleece)
- Thermal Underwear (Inner Top, Inner Bottom)

## Notes

- This is an MVP with basic authentication (global session variables)
- Production deployment requires database password updates and proper session management
- Tooltips on action buttons show "Accept", "Delay", "Reject" on hover
- Registration uses client-side and server-side validation for army number format (exactly 8 characters)

