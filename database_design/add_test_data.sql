-- ============================================================
-- Library Management System
-- Test Data
-- ============================================================
-- Users are intentionally excluded.
-- ============================================================


-- ============================================================
-- CUSTOMERS
-- ============================================================

INSERT INTO customers (
    customer_first_name,
    customer_surname,
    customer_email,
    customer_cell
)
VALUES
    ('John', 'Smith', 'john.smith@example.com', '0821234567'),
    ('Sarah', 'Johnson', 'sarah.johnson@example.com', '0832345678'),
    ('David', 'Williams', 'david.williams@example.com', '0843456789'),
    ('Emma', 'Brown', 'emma.brown@example.com', '0724567890'),
    ('James', 'Wilson', 'james.wilson@example.com', '0735678901'),
    ('Olivia', 'Taylor', 'olivia.taylor@example.com', '0746789012'),
    ('Daniel', 'Anderson', 'daniel.anderson@example.com', '0767890123'),
    ('Sophie', 'Thomas', 'sophie.thomas@example.com', '0788901234');


-- ============================================================
-- AUTHORS
-- ============================================================

INSERT INTO authors (
    author_first_name,
    author_surname
)
VALUES
    ('George', 'Orwell'),
    ('J.R.R.', 'Tolkien'),
    ('J.K.', 'Rowling'),
    ('Stephen', 'King'),
    ('Agatha', 'Christie'),
    ('Harper', 'Lee'),
    ('F. Scott', 'Fitzgerald'),
    ('Jane', 'Austen');


-- ============================================================
-- GENRES
-- ============================================================

INSERT INTO genres (
    genre_name,
    genre_descr
)
VALUES
    (
        'Dystopian',
        'Fiction depicting oppressive or undesirable societies.'
    ),
    (
        'Fantasy',
        'Fiction involving magic, mythical creatures and imaginary worlds.'
    ),
    (
        'Horror',
        'Fiction intended to frighten or unsettle the reader.'
    ),
    (
        'Mystery',
        'Fiction involving crimes, secrets and investigations.'
    ),
    (
        'Classic',
        'Literature recognised for its historical or cultural significance.'
    );


-- ============================================================
-- INVENTORY STATUS
-- ============================================================

INSERT INTO inventory_status (
    inventory_status_name,
    inventory_status_descr
)
VALUES
    (
        'Available',
        'Book is available to be loaned.'
    ),
    (
        'Loaned',
        'Book is currently loaned to a customer.'
    ),
    (
        'Damaged',
        'Book is damaged and currently unavailable.'
    ),
    (
        'Lost',
        'Book has been reported lost.'
    );


-- ============================================================
-- BOOKS
-- ============================================================

INSERT INTO books (
    book_name,
    book_descr,
    book_isbn,
    book_genre_id,
    book_author_id
)
VALUES

    (
        '1984',
        'A dystopian novel about surveillance and totalitarianism.',
        '9780451524935',
        (SELECT genre_id FROM genres WHERE genre_name = 'Dystopian'),
        (SELECT author_id FROM authors WHERE author_surname = 'Orwell')
    ),

    (
        'The Hobbit',
        'A fantasy adventure following Bilbo Baggins.',
        '9780547928227',
        (SELECT genre_id FROM genres WHERE genre_name = 'Fantasy'),
        (SELECT author_id FROM authors WHERE author_surname = 'Tolkien')
    ),

    (
        'Harry Potter and the Philosopher''s Stone',
        'The first novel in the Harry Potter series.',
        '9780747532699',
        (SELECT genre_id FROM genres WHERE genre_name = 'Fantasy'),
        (SELECT author_id FROM authors WHERE author_surname = 'Rowling')
    ),

    (
        'The Shining',
        'A horror novel about a family staying at an isolated hotel.',
        '9780307743657',
        (SELECT genre_id FROM genres WHERE genre_name = 'Horror'),
        (SELECT author_id FROM authors WHERE author_surname = 'King')
    ),

    (
        'Murder on the Orient Express',
        'Hercule Poirot investigates a murder aboard a train.',
        '9780062693662',
        (SELECT genre_id FROM genres WHERE genre_name = 'Mystery'),
        (SELECT author_id FROM authors WHERE author_surname = 'Christie')
    ),

    (
        'To Kill a Mockingbird',
        'A classic novel exploring justice and morality.',
        '9780061120084',
        (SELECT genre_id FROM genres WHERE genre_name = 'Classic'),
        (SELECT author_id FROM authors WHERE author_surname = 'Lee')
    ),

    (
        'The Great Gatsby',
        'A novel about wealth and ambition in 1920s America.',
        '9780743273565',
        (SELECT genre_id FROM genres WHERE genre_name = 'Classic'),
        (SELECT author_id FROM authors WHERE author_surname = 'Fitzgerald')
    ),

    (
        'Pride and Prejudice',
        'A classic novel about relationships and social expectations.',
        '9780141439518',
        (SELECT genre_id FROM genres WHERE genre_name = 'Classic'),
        (SELECT author_id FROM authors WHERE author_surname = 'Austen')
    );


-- ============================================================
-- BOOK INVENTORY
-- ============================================================

-- 1984 - 3 copies
INSERT INTO book_inventory (book_id, inventory_status_id)
SELECT
    b.book_id,
    s.inventory_status_id
FROM books b
CROSS JOIN inventory_status s
CROSS JOIN generate_series(1, 3)
WHERE b.book_name = '1984'
AND s.inventory_status_name = 'Available';


-- The Hobbit - 4 copies
INSERT INTO book_inventory (book_id, inventory_status_id)
SELECT
    b.book_id,
    s.inventory_status_id
FROM books b
CROSS JOIN inventory_status s
CROSS JOIN generate_series(1, 4)
WHERE b.book_name = 'The Hobbit'
AND s.inventory_status_name = 'Available';


-- Harry Potter - 5 copies
INSERT INTO book_inventory (book_id, inventory_status_id)
SELECT
    b.book_id,
    s.inventory_status_id
FROM books b
CROSS JOIN inventory_status s
CROSS JOIN generate_series(1, 5)
WHERE b.book_name = 'Harry Potter and the Philosopher''s Stone'
AND s.inventory_status_name = 'Available';


-- The Shining - 2 copies
INSERT INTO book_inventory (book_id, inventory_status_id)
SELECT
    b.book_id,
    s.inventory_status_id
FROM books b
CROSS JOIN inventory_status s
CROSS JOIN generate_series(1, 2)
WHERE b.book_name = 'The Shining'
AND s.inventory_status_name = 'Available';


-- Murder on the Orient Express - 3 copies
INSERT INTO book_inventory (book_id, inventory_status_id)
SELECT
    b.book_id,
    s.inventory_status_id
FROM books b
CROSS JOIN inventory_status s
CROSS JOIN generate_series(1, 3)
WHERE b.book_name = 'Murder on the Orient Express'
AND s.inventory_status_name = 'Available';


-- To Kill a Mockingbird - 3 copies
INSERT INTO book_inventory (book_id, inventory_status_id)
SELECT
    b.book_id,
    s.inventory_status_id
FROM books b
CROSS JOIN inventory_status s
CROSS JOIN generate_series(1, 3)
WHERE b.book_name = 'To Kill a Mockingbird'
AND s.inventory_status_name = 'Available';


-- The Great Gatsby - 2 copies
INSERT INTO book_inventory (book_id, inventory_status_id)
SELECT
    b.book_id,
    s.inventory_status_id
FROM books b
CROSS JOIN inventory_status s
CROSS JOIN generate_series(1, 2)
WHERE b.book_name = 'The Great Gatsby'
AND s.inventory_status_name = 'Available';


-- Pride and Prejudice - 3 copies
INSERT INTO book_inventory (book_id, inventory_status_id)
SELECT
    b.book_id,
    s.inventory_status_id
FROM books b
CROSS JOIN inventory_status s
CROSS JOIN generate_series(1, 3)
WHERE b.book_name = 'Pride and Prejudice'
AND s.inventory_status_name = 'Available';


-- ============================================================
-- BOOK LOANS
-- ============================================================

-- Current loan
INSERT INTO book_loans (
    customer_id,
    inventory_id,
    date_loaned,
    date_due,
    date_returned
)
VALUES (
    (SELECT customer_id
     FROM customers
     WHERE customer_email = 'john.smith@example.com'),

    (SELECT MIN(bi.inventory_id)
     FROM book_inventory bi
     JOIN books b ON b.book_id = bi.book_id
     WHERE b.book_name = '1984'),

    CURRENT_DATE - 5,
    CURRENT_DATE + 9,
    NULL
);


-- Current overdue loan
INSERT INTO book_loans (
    customer_id,
    inventory_id,
    date_loaned,
    date_due,
    date_returned
)
VALUES (
    (SELECT customer_id
     FROM customers
     WHERE customer_email = 'sarah.johnson@example.com'),

    (SELECT MIN(bi.inventory_id)
     FROM book_inventory bi
     JOIN books b ON b.book_id = bi.book_id
     WHERE b.book_name = 'The Hobbit'),

    CURRENT_DATE - 25,
    CURRENT_DATE - 11,
    NULL
);


-- Previously returned loan
INSERT INTO book_loans (
    customer_id,
    inventory_id,
    date_loaned,
    date_due,
    date_returned
)
VALUES (
    (SELECT customer_id
     FROM customers
     WHERE customer_email = 'david.williams@example.com'),

    (SELECT MIN(bi.inventory_id)
     FROM book_inventory bi
     JOIN books b ON b.book_id = bi.book_id
     WHERE b.book_name = 'The Shining'),

    CURRENT_DATE - 40,
    CURRENT_DATE - 26,
    CURRENT_DATE - 28
);


-- Previously returned late
INSERT INTO book_loans (
    customer_id,
    inventory_id,
    date_loaned,
    date_due,
    date_returned
)
VALUES (
    (SELECT customer_id
     FROM customers
     WHERE customer_email = 'emma.brown@example.com'),

    (SELECT MIN(bi.inventory_id)
     FROM book_inventory bi
     JOIN books b ON b.book_id = bi.book_id
     WHERE b.book_name = 'Pride and Prejudice'),

    CURRENT_DATE - 50,
    CURRENT_DATE - 36,
    CURRENT_DATE - 30
);


-- ============================================================
-- UPDATE CURRENTLY LOANED INVENTORY
-- ============================================================

UPDATE book_inventory
SET inventory_status_id = (
    SELECT inventory_status_id
    FROM inventory_status
    WHERE inventory_status_name = 'Loaned'
)
WHERE inventory_id IN (
    SELECT inventory_id
    FROM book_loans
    WHERE date_returned IS NULL
);


-- ============================================================
-- SET ONE BOOK AS DAMAGED
-- ============================================================

UPDATE book_inventory
SET inventory_status_id = (
    SELECT inventory_status_id
    FROM inventory_status
    WHERE inventory_status_name = 'Damaged'
)
WHERE inventory_id = (
    SELECT MAX(bi.inventory_id)
    FROM book_inventory bi
    JOIN books b ON b.book_id = bi.book_id
    WHERE b.book_name = 'The Shining'
);


-- ============================================================
-- SET ONE BOOK AS LOST
-- ============================================================

UPDATE book_inventory
SET inventory_status_id = (
    SELECT inventory_status_id
    FROM inventory_status
    WHERE inventory_status_name = 'Lost'
)
WHERE inventory_id = (
    SELECT MAX(bi.inventory_id)
    FROM book_inventory bi
    JOIN books b ON b.book_id = bi.book_id
    WHERE b.book_name = '1984'
);