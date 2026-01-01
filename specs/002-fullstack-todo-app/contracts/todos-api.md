# API Contract: Todos API

**Base URL**: `/api/v1`
**Format**: JSON

## Endpoints

### 1. List Todos
- **Method**: `GET`
- **Path**: `/todos`
- **Auth**: Required
- **Response (200 OK)**:
  ```json
  [
    {
      "id": "uuid",
      "title": "Buy milk",
      "is_completed": false,
      "created_at": "iso-date"
    }
  ]
  ```

### 2. Create Todo
- **Method**: `POST`
- **Path**: `/todos`
- **Auth**: Required
- **Body**:
  ```json
  {
    "title": "New Task"
  }
  ```
- **Response (201 Created)**: Created Todo object

### 3. Update Todo
- **Method**: `PATCH`
- **Path**: `/todos/{id}`
- **Auth**: Required
- **Body**:
  ```json
  {
    "title": "Updated Task",
    "is_completed": true
  }
  ```
- **Response (200 OK)**: Updated Todo object

### 4. Delete Todo
- **Method**: `DELETE`
- **Path**: `/todos/{id}`
- **Auth**: Required
- **Response (204 No Content)**: Successfully deleted

## Errors
- `401 Unauthorized`: Missing or invalid session
- `403 Forbidden`: Attempting to access/modify another user's todo
- `422 Unprocessable Entity`: Validation failure (empty title, etc.)
- `404 Not Found`: Item does not exist
