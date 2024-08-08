
# Database Seeder Script

This document explains the functionality of the database seeder script. The script is used to populate the MongoDB database with fake data for testing and development purposes. It uses the `Faker` library to generate random data and `argparse` to handle command-line arguments for different seeding options.

## Environment Variables
Create a .env file in the root directory of your project with the following content:

   ```bash
    MONGODB_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/<dbname>?retryWrites=true&w=majority
    DB_NAME=<dbname>
   ```
Replace "username", "password", and "dbname" with your MongoDB credentials and database name.


## Usage

The script provides three main functionalities:
1. **Seed the database only if it is empty** (default behavior).
2. **Reset the database and seed it** using the `--reset` flag.
3. **Force seed the database without resetting** using the `--force` flag.

### Running the Script

1. **Default Behavior (Seed only if the database is empty)**:

   ```bash
   python seeder.py
   ```

   This will check if the database collections (`authors`, `books`, `reviews`, `sales`) are empty. If they are, it will seed the database with the generated data. If the collections are not empty, it will not perform any action.

2. **Reset and Seed**:

   ```bash
   python seeder.py --reset
   ```

   This will clear all the data in the `authors`, `books`, `reviews`, and `sales` collections and then seed the database with new generated data.

3. **Force Seed without Resetting**:

   ```bash
   python seeder.py --force
   ```

   This will seed the database with the generated data without resetting it, even if the collections are not empty.

### Command-Line Arguments

- `--reset`: Clears all the collections in the database before seeding.
- `--force`: Seeds the database even if the collections are not empty.

## Script Explanation

The seeder script performs the following steps:

1. **Connect to MongoDB**: 
   Uses the `MongoClient` from `pymongo` and connects to the database using the URI and database name specified in the environment variables.

2. **Initialize Faker**: 
   Initializes the `Faker` library to generate random data.

3. **Reset Database**: 
   A function `reset_database` to clear all the collections in the database.

4. **Check if Database is Empty**: 
   A function `database_is_empty` to check if all the collections are empty.

5. **Generate and Insert Data**:
   - Creates 50 authors with random data.
   - Creates 300 books, each associated with a random author.
   - Creates between 1 to 10 reviews for each book.
   - Creates sales data for each book over a span of 5 years.

6. **Command-Line Argument Parsing**: 
   Uses `argparse` to handle `--reset` and `--force` flags for different seeding behaviors.


