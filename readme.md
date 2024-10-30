# API Documentation

### Authentication
- Most endpoints require JWT-based authentication. Include the following header in each request that requires authentication:

```bash
Authorization: Bearer <access_token>
```
To get access_token and refresh_token, use the Login endpoint.

### 1. User Detail

- **URL:** /auth/user/<int:pk>/
- **Method:** GET
- **Authorization:** Required (JWT token)
- **Response Status:** 200 OK
- **Response Body:**
```bash
{
    "id": 1,
    "username": "exampleuser",
    "role": "Member",
    "email": "email",
}
```


### 2. Login (Token Obtain)
- **URL:** /auth/token/
- **Method:** POST
- **Authorization:** None
- **Request Body Content-Type:** application/json
- **Fields:**
```bash
{
    "username": "exampleuser",
    "password": "password123"
}
```
- **Response Status:** 200 OK or 401 Unauthorized
**Response Body:**
```bash
{
    "username": "exampleuser",
    "role": "Member",
    "id": 1,
    "access": "<access_token>",
    "refresh": "<refresh_token>"
}
```

### 1. Token Refresh
- **URL:** /auth/token/refresh/
- **Method:** POST
- **Authorization:** None
- **Request Body Content-Type:** application/json
- **Fields:**
```bash
{
    "refresh": "<refresh_token>"
}
```
- **Response Status:** 200 OK
- **Response Body:**
```bash
{
    "access": "<new_access_token>"
}
```

### 1. Logout

- **URL:** /auth/token/logout/
- **Method:** POST
- **Authorization:** Required
- **Request Body Content-**Type: application/json
- **Fields:**

```bash
{
    "refresh_token": "<refresh_token>"
}
```

- **Response Status:** 205 Reset Content
- **Response Body:**
```bash
{
    "message": "Successfully logged out"
}
```

### 1. Signup

- **URL:** /auth/signup/
- **Method:** POST
- **Authorization:** None or Superuser (for Sub Admin and Superuser roles)
- **Request Body Content-Type:** application/json
- **Fields:**
```bash
{
    "username": "newuser",
    "password": "password123",
    "email": "newuser@example.com",
    "role": "Member"  // Options: "Member", "Sub Admin", "Superuser"
}
```
- **Response Status:** 201 Created or 403 Forbidden for unauthorized role assignments
- **Response Body:**
```bash
{
    "message": "User created successfully"
}
```
### 1. User Profile
- **URL:** /auth/profile/
- **Methods:** GET, PUT, DELETE
- **Authorization:** Required
#### GET User Profile
- **Response Body:**
```bash
{
    "id": 1,
    "username": "exampleuser",
    "role": "Member",
    // Other user details
}
```
#### PUT Update Profile
- **Request Body:**
```bash
{
    "email": "newemail@example.com",
    "password": "newpassword123"
}
```
- **Response Body:**
```bash
{
    "id": 1,
    "username": "exampleuser",
    "email": "newemail@example.com",
    "role": "Member",
    // Updated user details
}
```
#### DELETE User Profile
- **Response Body:**
```bash
{
    "message": "User deleted successfully"
}
```

### 1. List All Users
- **URL:** /auth/users/
- **Method:** GET
- **Authorization:** Required
- **Response Status:** 200 OK
- **Response Body:**
```bash
[
    {
        "id": 1,
        "username": "user1",
        "role": "Member"
    },
    {
        "id": 2,
        "username": "user2",
        "role": "Sub Admin"
    }
]
```


### 1. List All Sub Admins
- **URL:** /auth/users/sub_admins/
- **Method:** GET
- **Authorization:** Required
- **Response Status:** 200 OK
- **Response Body:**
```bash
[
    {
        "id": 2,
        "username": "subadmin1",
        "role": "Sub Admin"
    }
]
```

### 1. List All Members
- **URL:** /auth/users/members/
- **Method:** GET
- **Authorization:** Required
**Response Status:** 200 OK
- **Response Body:**
```bash
[
    {
        "id": 3,
        "username": "member1",
        "role": "Member"
    }
]
```

# Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/N16H7H4WK-3R/anpr.git
   ```

2. Navigate to the project directory:
    ```bash
    cd anpr
    ```

3. Create a Virtual Environement:
   - install python virtual env (venv) module and then, 
    ```bash
    python3 -m venv env
    ```

4. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5. Migrate the database:
   ```bash
   python manage.py migrate
   ```

6. Run the Django Server
    ```bash
    python manage.py runserver
    ```

