## Database Schema Documentation

This documentation provides an overview of the database schema and associated functionalities for the application.

### 1. State

**Table Name:** `states`

**Columns:**
1. `id` (Primary Key, Autoincrement)
2. `name` (Text, Not Null, Unique)
3. `country` (Text, Not Null)

#### Functions:

1. **`create_state(name, country)`**
   - Adds a new state to the database.

2. **`get_state_details(state_id)`**
   - Retrieves details about a specific state.

3. **`delete_state(state_id)`**
   - Removes a state and its associated data (if any).

### 2. City

**Class Name:** `City`

**Table Name:** `cities`

**Columns:**
1. `id` (Primary Key, Autoincrement)
2. `name` (Text, Not Null)
3. `state` (Text, Not Null)
4. `country` (Text, Not Null)

#### Functions:

1. **`create_city()`**
   - Creates the city table if it doesn't exist.
   - Inserts a new city into the database.

2. **`get_city_details(city_id)`**
   - Retrieves details about a specific city.

3. **`delete_city(city_id)`**
   - Removes a city and its associated data (if any).

### 3. Place

**Table Name:** `places`

**Columns:**
1. `id` (Primary Key, Autoincrement)
2. `title` (Text, Not Null)
3. `description` (Text)
4. `location` (Text, Not Null)
5. `price` (Real, Not Null)
6. `amenities` (Text)
7. `photos` (Text)
8. `availability_calendar` (Text)
9. `host_id` (Integer, Not Null)
10. `reviews` (JSON)

#### Functions:

1. **`create_place(title, description, location, price, amenities, photos, availability_calendar, host_id, reviews)`**
   - Adds a new place to the database.

2. **`get_place_details(place_id)`**
   - Retrieves detailed information about a place.

3. **`edit_place(place_id, **kwargs)`**
   - Modifies existing place information.

4. **`delete_place(place_id)`**
   - Removes a place listing.

5. **`user_add_place(user_id, title, description, location, price, amenities, photos, availability_calendar)`**
   - Allows a user to add their place for listing.

### 4. Amenity

**Table Name:** `Amenity`

**Columns:**
1. `id` (Primary Key, Autoincrement)
2. `name` (Text, Not Null, Unique)
3. `description` (Text)

#### Functions:

1. **`create_amenity(name, description)`**
   - Adds a new amenity to the database.

2. **`get_amenity_details(amenity_id)`**
   - Retrieves details about a specific amenity.

3. **`delete_amenity(amenity_id)`**
   - Removes an amenity from the system.

### 5. Review

**Table Name:** `Review`

**Columns:**
1. `id` (Primary Key, Autoincrement)
2. `content` (Text, Not Null)
3. `rating` (Integer, Not Null)
4. `author_id` (Integer, Not Null, Foreign Key: User.id)
5. `place_id` (Integer, Not Null, Foreign Key: Place.id)

#### Functions:

1. **`create_review(content, rating, author_id, place_id)`**
   - Adds a new review to the database.

2. **`get_place_reviews(place_id)`**
   - Retrieves reviews for a specific place.

3. **`delete_review(review_id)`**
   - Removes a user's review.

### 6. User

**Class Name:** `User`

**Table Name:** `users`

**Columns:**
1. `id` (Primary Key, Autoincrement)
2. `email` (Text, Unique, Not Null)
3. `password` (Text, Not Null)
4. `name` (Text, Not Null)
5. `profile_picture` (Text)

#### Functions:

1. **`create_user()`**
   - Creates the user table if it doesn't exist.
   - Inserts a new user into the database.

2. **`authenticate_user(email, password)`**
   - Authenticates a user based on email and password.

3. **`update_user()`**
   - Updates user information.

4. **`delete_user()`**
   - Deletes a user from the database based on email.

This schema and associated functions form the backbone of the application's data structure, facilitating the storage and retrieval of information related to states, cities, places, amenities, reviews, and users.