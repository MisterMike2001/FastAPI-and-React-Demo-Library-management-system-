CREATE TABLE users (
    user_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    user_first_name VARCHAR(100) NOT NULL,
    user_surname VARCHAR(100) NOT NULL,
    user_email VARCHAR(255) NOT NULL UNIQUE,
    user_cell VARCHAR(20)
);


CREATE TABLE customers (
    customer_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_first_name VARCHAR(100) NOT NULL,
    customer_surname VARCHAR(100) NOT NULL,
    customer_email VARCHAR(255) NOT NULL UNIQUE,
    customer_cell VARCHAR(20)
);


CREATE TABLE authors (
    author_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    author_first_name VARCHAR(100) NOT NULL,
    author_surname VARCHAR(100) NOT NULL
);


CREATE TABLE genres (
    genre_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    genre_name VARCHAR(100) NOT NULL UNIQUE,
    genre_descr VARCHAR(255) NOT NULL
);


CREATE TABLE books (
    book_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    book_name VARCHAR(100) NOT NULL,
    book_descr VARCHAR(255) NOT NULL,
    book_isbn VARCHAR(20) UNIQUE,
    book_genre_id INTEGER NOT NULL,
    book_author_id INTEGER NOT NULL,

    CONSTRAINT fk_book_genre
        FOREIGN KEY (book_genre_id)
        REFERENCES genres(genre_id),

    CONSTRAINT fk_book_author
        FOREIGN KEY (book_author_id)
        REFERENCES authors(author_id)
);


CREATE TABLE inventory_status (
    inventory_status_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    inventory_status_name VARCHAR(100) NOT NULL UNIQUE,
    inventory_status_descr VARCHAR(255) NOT NULL
);


CREATE TABLE book_inventory (
    inventory_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    book_id INTEGER NOT NULL,
    inventory_status_id INTEGER NOT NULL,

    CONSTRAINT fk_book_inventory_book
        FOREIGN KEY (book_id)
        REFERENCES books(book_id),

    CONSTRAINT fk_book_inventory_status
        FOREIGN KEY (inventory_status_id)
        REFERENCES inventory_status(inventory_status_id)
);


CREATE TABLE book_loans (
    loan_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    inventory_id INTEGER NOT NULL,
    date_loaned DATE NOT NULL,
    date_due DATE NOT NULL,
    date_returned DATE,

    CONSTRAINT fk_book_loans_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id),

    CONSTRAINT fk_book_loans_inventory
        FOREIGN KEY (inventory_id)
        REFERENCES book_inventory(inventory_id)
);