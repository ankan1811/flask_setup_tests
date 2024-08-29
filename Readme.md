### Instructions for environment setup:

## Overview

This project provides a simple API to manage and report on transactions related to lawn mowing services. It allows you to upload transactions, and generate reports on gross revenue, expenses, and net revenue.

## Instructions for Environment Setup

Follow these steps to set up and run the project:

### 1. After navigating to the root directory, Create a Virtual Environment

Creating a virtual environment ensures consistency in package versions:

```
pip install virtualenv
python -m virtualenv venv
```

##### To activate the virtual environment:

```
Windows:
venv\Scripts\activate
macOS/Linux:
source venv/bin/activate
```

### 2. Then we can install all the packages from the requirements.txt file using:-

`pip install -r requirements.txt`

### 3. For running the server then we can use:-

`flask run`

### 4. For database connection we can use the flask shell using the command:-

` flask shell`

##### Then inside the shell we can write:-

```
from src.database import db
db.create_all()
#This will create the Transaction table.
```

### 5. We have tests in the tests.py file in the root directory and for running the tests we can simply use the command:-

```
python -m unittest tests.py
```

## API Endpoints

### POST /transactions

Uploads a CSV file of transactions. The file should be formatted as follows:

- **Date**: Transaction date (YYYY-MM-DD)
- **Type**: Either "Income" or "Expense"
- **Amount**: Transaction amount in dollars
- **Memo**: Description or category

#### Response

- **Success**: `200 OK` with a message indicating the number of rows processed and any invalid rows.
- **Error**: `400 Bad Request` if there are issues with the file upload.

### GET /report

Generates a report of the transactions.

#### Response

A JSON document with the following structure:

```json
{
    "gross-revenue": <amount>,
    "expenses": <amount>,
    "net-revenue": <amount>
}
```

## Additional Context

### Solution and Approach

This solution provides a basic API for managing and reporting transactions. The approach taken involves:

1. **Flask Application**: I have used Python and flask for this task.
2. **Database Integration**: SQLAlchemy was used for database interactions, and an SQLite in-memory database was utilized for testing and development purposes.
3. **CSV Upload**: Transactions are uploaded via a CSV file. The file is parsed, and valid transactions are stored in the database. Invalid rows are identified and reported.
4. **Reporting**: I used this endpoint to generate financial reports based on the stored transactions.

### Assumptions Made

- **CSV Format**: It is assumed that the uploaded CSV file follows the specified format and includes valid data for parsing.
- **Single Table**: The transactions are stored in a single table (`Transaction`), which is sufficient for the current scope.
- **Memory Storage for Tests**: An in-memory SQLite database is used for testing, assuming that this approach is acceptable for test isolation and performance.

## Shortcomings of the Solution

1. **No Authentication or Authorization**: The current API does not include authentication or authorization, meaning that any user can upload transactions or access reports without restriction.
2. **Hardcoded CSV Structure**: My solution assumes a fixed CSV structure. Variations in file format or additional fields are not supported.
3. **Scalability**: Using an SQLite in-memory database is suitable for testing but may not scale well for production use. A more robust database system might be needed (probably postgreSql should do).

## Future Improvements

If additional time were available, the following enhancements would be considered:

1. **Authentication and Authorization**: I will implement user authentication and authorization to restrict access to the API endpoints.
2. **Flexible CSV Parsing**: I will introduce support for different CSV structures or file formats to make the system more adaptable.
3. **Database Optimization**: Use a more scalable database solution for production environments, such as PostgreSQL, to handle larger datasets, and improve performance by methods like indexing on the database.
