CREATE TABLE IF NOT EXISTS poly_organization (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    status TINYINT NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

    CREATE TABLE IF NOT EXISTS poly_users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255) NOT NULL,
        status TINYINT NOT NULL DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

CREATE TABLE IF NOT EXISTS poly_user_organization (    
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    organization_id INT NOT NULL,
    Constraint FOREIGN KEY (user_id) REFERENCES poly_users(id),
    Constraint FOREIGN KEY (organization_id) REFERENCES poly_organization(id)
);