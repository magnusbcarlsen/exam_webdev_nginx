BEGIN;

-- Create roles table
CREATE TABLE roles (
    role_pk TEXT PRIMARY KEY,
    role_name TEXT
);

-- Insert values into roles table
INSERT INTO roles (role_pk, role_name) VALUES ('0', 'customer');
INSERT INTO roles (role_pk, role_name) VALUES ('1', 'partner');
INSERT INTO roles (role_pk, role_name) VALUES ('2', 'admin');

-- Create users table
CREATE TABLE users (
    user_pk TEXT PRIMARY KEY,
    user_role_fk TEXT REFERENCES roles(role_pk) ON DELETE CASCADE,
    user_username TEXT,
    user_name TEXT,
    user_last_name TEXT,
    user_email TEXT UNIQUE,
    user_password TEXT,
    user_is_blocked TEXT DEFAULT '0',
    user_is_verified TEXT DEFAULT '0',
    user_created_at TIMESTAMP DEFAULT now(),
    user_updated_at TIMESTAMP DEFAULT now(),
    user_deleted_at TEXT DEFAULT '0'
);

SELECT * FROM users;    

-- Insert values into users table
INSERT INTO users (user_pk, user_role_fk, user_username, user_name, user_last_name, user_email, user_password, user_is_blocked, user_is_verified, user_created_at, user_updated_at, user_deleted_at) VALUES
('1', '1', 'dirty_ranch', 'ole', 'olesen', 'ole@partner.dk', '12345678', '0', '1', '2024-06-03 09:03:13', '2024-06-03 09:03:13', '0'),
('2', '0', 'cowboy', 'anders', 'andersen', 'anders@customer.dk', '12345678', '0', '0', '2024-06-03 09:03:13', '2024-06-03 09:03:13', '0'),
('3', '2', 'admin', 'admin', 'adminson', 'admin@company.dk', '12345678', '0', '1', '2024-06-03 09:03:13', '2024-06-03 09:03:13', '0');

-- Create properties table
CREATE TABLE properties (
    property_pk TEXT PRIMARY KEY,
    property_user_fk TEXT REFERENCES users(user_pk) ON DELETE CASCADE,
    property_booking_fk TEXT,
    property_name TEXT,
    property_description TEXT,
    property_price_pr_night REAL,
    property_images TEXT,
    property_rating REAL,
    property_address TEXT,
    property_country TEXT,
    property_postal_code TEXT,
    property_lat TEXT,
    property_lon TEXT,
    property_is_blocked TEXT,
    property_created_at TIMESTAMP DEFAULT now(),
    property_updated_at TIMESTAMP DEFAULT now(),
    property_deleted_at TEXT DEFAULT '0'
);

-- Insert values into properties table
INSERT INTO properties (property_pk, property_user_fk, property_booking_fk, property_name, property_description, property_price_pr_night, property_images, property_rating, property_address, property_country, property_postal_code, property_lat, property_lon, property_is_blocked, property_created_at, property_updated_at, property_deleted_at) VALUES
('1', '1', '0', 'Pretty beach house', 'Nestled along the pristine coastline, the Pretty Beach House offers breathtaking ocean views and serene surroundings. This charming abode features a spacious open-plan living area, tastefully decorated with coastal-inspired furnishings. Guests can enjoy morning coffee on the large deck, take leisurely strolls along the sandy shore, and unwind in the peaceful ambiance of this seaside retreat.', 489.0, '1.webp,1-1.jpeg,1-2.webp,1-3.jpeg,1-4.webp', 4.5, 'Borgergade 45, Copenhagen', 'Denmark', '1300', '12.5683', '55.6761', '0', '2024-06-03 09:03:13', '2024-06-03 09:03:13', '0'),
('10', '1', '0', 'Lake-Side Home', 'The Lake-Side Home is a tranquil haven set against the backdrop of a serene lake. The property features spacious living areas with panoramic lake views, a well-equipped kitchen, and comfortable bedrooms. Guests can enjoy activities like kayaking, fishing, or simply relaxing by the water, soaking in the natural beauty of the surroundings.', 350.0, '10.webp,10-1.webp,10-2.jpeg,10-3.jpeg,10-4.jpeg', 4.8, 'Fjordvej 68, Fredericia', 'Denmark', '7000', '10.4024', '55.4038', '0', '2024-06-03 09:03:13', '2024-06-03 09:03:13', '0'),
('2', '1', '0', 'Apartment in the Eye of Copenhagen', 'Located in the heart of Copenhagen, this modern apartment provides the perfect urban escape. With sleek, contemporary design and state-of-the-art amenities, the space offers comfort and convenience. Guests are just steps away from world-class dining, shopping, and cultural attractions, making it an ideal base for exploring the vibrant city.', 359.0, '2.webp,2-1.webp,2-2.webp,2-3.jpeg,2-4.webp', 4.8, 'Algade 23, Aarhus', 'Denmark', '8000', '12.5012', '55.7095', '0', '2024-06-03 09:03:13', '2024-06-03 09:03:13', '0'),
('3', '1', '0', 'House Down by the Sea', 'The House Down by the Sea is a picturesque seaside home that promises tranquility and relaxation. Featuring spacious interiors, this property boasts large windows that frame stunning sea views. The outdoor area includes a private garden and direct beach access, making it perfect for family gatherings or romantic getaways.', 800.0, '3.webp,3-1.webp,3-2.jpeg,3-3.jpeg,3-4.jpeg', 4.1, 'Vestergade 7, Odense', 'Denmark', '5000', '10.3869', '55.3967', '0', '2024-06-03 09:03:13', '2024-06-03 09:03:13', '0'),
('4', '1', '0', 'Cafe Apartment Near Nyhavn', 'This charming apartment, located near the iconic Nyhavn canal, exudes a cozy and inviting atmosphere. The space combines classic Danish design with modern comforts, offering a fully equipped kitchen and comfortable living area. Guests can enjoy the vibrant café culture of Nyhavn, with its colorful buildings and bustling waterfront.', 918.0, '4.webp,4-1.jpeg,4-2.webp,4-3.webp,4-4.jpeg', 4.2, 'Havnegade 39, Esbjerg', 'Denmark', '6700', '9.9217', '55.4663', '0', '2024-06-03 09:03:13', '2024-06-03 09:03:13', '0'),
('5', '1', '0', 'Room in Famous Danish Bathing Hotel', 'Experience the charm of a historic Danish bathing hotel with a stay in this beautifully appointed room. The property retains its old-world elegance while providing modern amenities for a comfortable stay. Guests can indulge in spa treatments, savor gourmet dining, and explore the picturesque surroundings.', 479.0, '5.webp,5-1.webp,5-2.jpeg,5-3.jpeg,5-4.jpeg', 4.6, 'Østergade 21, Aalborg', 'Denmark', '9000', '9.554', '55.6776', '0', '2024-06-03 09:03:13', '2024-06-03 09:03:13', '0'),
('6', '1', '0', 'Two Chairs in Little Beach House', 'This quaint little beach house, complete with two comfortable chairs on the porch, is the perfect retreat for couples or solo travelers seeking peace and simplicity. The cozy interiors feature rustic décor and all the essentials for a relaxing stay. Enjoy sunsets from the porch or take a short walk to the nearby beach.', 345.0, '6.webp,6-1.jpeg,6-2.jpeg,6-3.webp,6-4.jpeg', 4.5, 'Nørregade 30, Randers', 'Denmark', '8900', '8.51', '55.3911', '0', '2024-06-03 09:03:13', '2024-06-03 09:03:13', '0'),
('7', '1', '0', 'West-Side Beach House', 'The West-Side Beach House offers a luxurious escape with stunning views of the western coastline. This spacious property features modern architecture, high-end finishes, and ample outdoor space for entertaining. Whether lounging by the private pool or enjoying sunset dinners on the terrace, guests are sure to have an unforgettable stay.', 899.0, '7.webp,7-1.webp,7-2.webp,7-3.jpeg,7-4.jpeg', 3.9, 'Bredgade 76, Kolding', 'Denmark', '6000', '8.4467', '55.4668', '0', '2024-06-03 09:03:13', '2024-06-03 09:03:13', '0'),
('8', '1', '0', 'Renovated Apartment Near Amager', 'Situated in the trendy Amager district, this renovated apartment combines style and convenience. The interiors are thoughtfully designed with chic furnishings and modern amenities. Guests can explore nearby parks, visit the bustling local markets, and enjoy the vibrant nightlife of Amager.', 789.0, '8.webp,8-1.webp,8-2.jpeg,8-3.jpeg,8-4.webp', 2.2, 'Kirkegade 43, Vejle', 'Denmark', '7100', '8.5136', '55.7051', '0', '2024-06-03 09:03:13', '2024-06-03 09:03:13', '0'),
('9', '1', '0', 'Family Vacation Sea-House', 'Perfect for family vacations, this sea-house offers ample space and a host of amenities for all ages. The property includes multiple bedrooms, a large kitchen, and a cozy living area. Outdoors, guests can enjoy a private garden, play area, and direct access to the beach, making it an ideal spot for fun-filled family holidays.', 239.0, '9.webp,9-1.jpeg,9-2.jpeg,9-3.webp,9-4.webp', 4.1, 'Park Alle 34, Horsens', 'Denmark', '8700', '9.9716', '55.5863', '0', '2024-06-03 09:03:13', '2024-06-03 09:03:13', '0');

-- Create bookings table
CREATE TABLE bookings (
    booking_pk TEXT PRIMARY KEY,
    booking_user_fk TEXT REFERENCES users(user_pk) ON DELETE CASCADE,
    booking_property_fk TEXT REFERENCES properties(property_pk) ON DELETE CASCADE,
    booking_created_at TIMESTAMP DEFAULT now(),
    booking_deleted_at TEXT DEFAULT '0'
);

-- Create trigger to update property_booking_fk after insert on bookings
CREATE OR REPLACE FUNCTION update_property_booking_fk() RETURNS TRIGGER AS $$
BEGIN
    UPDATE properties
    SET property_booking_fk = NEW.booking_pk
    WHERE property_pk = NEW.booking_property_fk;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_property_booking_fk
AFTER INSERT ON bookings
FOR EACH ROW
EXECUTE FUNCTION update_property_booking_fk();

COMMIT;