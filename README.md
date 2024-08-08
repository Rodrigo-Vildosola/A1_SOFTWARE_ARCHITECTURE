# A1 Software Architecture



## Prerequisites

- Python 3.8+
- MongoDB

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Rodrigo-Vildosola/A1_SOFTWARE_ARCHITECTURE.git
cd A1_SOFTWARE_ARCHITECTURE
```

### 2. Create and Activate a Virtual Environment

#### On Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### On macOS and Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory of the project and add your MongoDB URI and database name:

```
MONGODB_URI=mongodb://localhost:27017
DB_NAME=your_db_name
```


### 5. Seed the Database

The seeder script can populate the database with fake data. By default, it will only seed the database if it is empty. Use the `--reset` flag to clear the database before seeding or the `--force` flag to seed regardless of the database state.

```bash
python seeder.py
```

To reset the database before seeding:

```bash
python seeder.py --reset
```

To force seed without resetting:

```bash
python seeder.py --force
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

Open your web browser and navigate to `http://127.0.0.1:8000/` to view the application.

