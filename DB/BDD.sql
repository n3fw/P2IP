DROP DATABASE IF EXISTS jardinage_exchange;
CREATE DATABASE jardinage_exchange;
USE jardinage_exchange;


CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    firstname VARCHAR(100) NOT NULL,
    lastname VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    city VARCHAR(100),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);


CREATE TABLE listings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    category_id INT NOT NULL,
    title VARCHAR(150) NOT NULL,
    description TEXT,
    tool_condition ENUM('neuf','bon_etat','use') NOT NULL,
    status ENUM('active','exchanged') DEFAULT 'active',

    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (category_id) REFERENCES categories(id)
);


CREATE TABLE listing_images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    listing_id INT NOT NULL,
    image_url TEXT NOT NULL,
    is_main BOOLEAN DEFAULT FALSE,

    FOREIGN KEY (listing_id) REFERENCES listings(id)
);


CREATE TABLE exchange_offers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    listing_id INT NOT NULL,
    sender_id INT NOT NULL,
    proposed_item VARCHAR(150),
    message TEXT,
    status ENUM('pending','accepted','refused'),

    FOREIGN KEY (listing_id) REFERENCES listings(id),
    FOREIGN KEY (sender_id) REFERENCES users(id)
);


CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    listing_id INT NOT NULL,
    sender_id INT NOT NULL,
    receiver_id INT NOT NULL,
    content TEXT,

    FOREIGN KEY (listing_id) REFERENCES listings(id),
    FOREIGN KEY (sender_id) REFERENCES users(id),
    FOREIGN KEY (receiver_id) REFERENCES users(id)
);


CREATE TABLE favorites (
    user_id INT,
    listing_id INT,

    PRIMARY KEY (user_id, listing_id),

    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (listing_id) REFERENCES listings(id)
);


CREATE TABLE reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    exchange_offer_id INT,
    author_id INT,
    target_user_id INT,
    rating INT,
    comment TEXT,

    FOREIGN KEY (exchange_offer_id) REFERENCES exchange_offers(id),
    FOREIGN KEY (author_id) REFERENCES users(id),
    FOREIGN KEY (target_user_id) REFERENCES users(id)
);


INSERT INTO users (firstname, lastname, email, password_hash, city) VALUES
('Martin','Dupont','martin.dupont@mail.com','mdp123','Paris'),
('David','Martinez','david.martinez@mail.com','mdp456','Lyon'),
('John','Snow','john.snow@mail.com','mdp789','Marseille');


INSERT INTO categories (name) VALUES
('Tondeuse'),
('Pelle'),
('Taille-haie'),
('Râteau');


INSERT INTO listings (user_id, category_id, title, description, tool_condition, status) VALUES
(1,1,'Tondeuse Bosch','Très bon état','bon_etat','active'),
(2,2,'Pelle Fiskars','Comme neuve','neuf','active'),
(3,3,'Taille-haie Ryobi','Fonctionnel','use','exchanged'),
(1,4,'Râteau jardin','Bon état','bon_etat','active');


INSERT INTO listing_images (listing_id, image_url, is_main) VALUES
(1,'tondeuse.jpg',TRUE),
(2,'pelle.jpg',TRUE),
(3,'taillehaie.jpg',TRUE),
(4,'rateau.jpg',TRUE);


INSERT INTO exchange_offers (listing_id, sender_id, proposed_item, message, status) VALUES
(1,2,'Pelle Fiskars','Je propose ma pelle','pending'),
(1,3,'Taille-haie Ryobi','Proposition échange','accepted'),
(2,1,'Râteau jardin','Je propose mon râteau','refused');


INSERT INTO messages (listing_id, sender_id, receiver_id, content) VALUES
(1,2,1,'Votre tondeuse est-elle disponible ?'),
(1,1,2,'Oui elle est disponible'),
(2,1,2,'Votre pelle m’intéresse');


INSERT INTO favorites VALUES
(1,2),
(2,1),
(3,1),
(3,4);


INSERT INTO reviews (exchange_offer_id, author_id, target_user_id, rating, comment) VALUES
(2,1,3,5,'Très bon échange avec John'),
(3,2,1,4,'Contact agréable avec Martin');


##REQUETES##

#AFFICHER LES ANNONCES ACTIVES
SELECT * FROM listings
WHERE status = 'active';

#RETOURNER LES ANNONCES D4UN UTILISATEUR
SELECT listings.title, users.firstname, users.lastname FROM listings
JOIN users ON listings.user_id = users.id;

#PERMETTRE A L4UTILISATEUR DE VOIR SES FAVORIS
SELECT listings.title, categories.name FROM favorites
JOIN listings ON favorites.listing_id = listings.id
JOIN categories ON listings.category_id = categories.id
JOIN users ON favorites.user_id = users.id
WHERE users.firstname = 'David'
AND users.lastname = 'Martinez';

#VOIR LES OFFRES RECU POUR UNE ANNONCE
SELECT exchange_offers.proposed_item, exchange_offers.message FROM exchange_offers
JOIN listings ON exchange_offers.listing_id = listings.id
WHERE listings.title = 'Tondeuse Bosch';

