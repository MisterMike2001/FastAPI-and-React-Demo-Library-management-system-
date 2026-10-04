# Database Design

This folder contains the PostgreSQL database scripts required to set up the database for the Library Management System.

## Database

The application uses **PostgreSQL** as its database.

## Setup

The scripts should be executed in the following order:

### 1. Create Database Tables

Run:

`tables_create_script.sql`

This script creates all tables, relationships, primary keys, foreign keys, and other constraints required by the application.

### 2. Add Test Data

Run:

`test_data.sql`

This script populates the database with test data that can be used during development and testing.

Test data is created for all relevant tables **except the `users` table**. Users should be created through the application so that authentication details, including passwords, are handled correctly.

## Important

Always run `tables_create_script.sql` before `test_data.sql`, as the test data depends on the database tables and relationships already existing.
