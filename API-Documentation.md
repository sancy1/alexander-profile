# API Documentation

## Overview

This document provides comprehensive API endpoint documentation for the Alexander Cyril Portfolio backend application, covering the **user_account** and **contact** applications.

**Base URL:** `http://localhost:8000` (development) or `https://alexandercyril.onrender.com` (production)

**Authentication:** Most endpoints require JWT authentication via Bearer token in the Authorization header.

---

SWAGGER
http://127.0.0.1:8000/swagger/schema/

## Table of Contents

1. [User Account App Endpoints](#user-account-app-endpoints)
   - [Authentication](#authentication)
   - [User Registration](#user-registration)
   - [Profile Management](#profile-management)
   - [Password Management](#password-management)
   - [User Management (Admin)](#user-management-admin)
2. [Contact App Endpoints](#contact-app-endpoints)
   - [Contact Form](#contact-form)
   - [Newsletter Management](#newsletter-management)
3. [Missing Endpoints & Implementation Notes](#missing-endpoints-implementation-notes)

---

## User Account App Endpoints

### Authentication

#### POST /api/user/auth/google/
**Description:** Authenticate user using Google OAuth2.

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "access_token": "google_oauth_access_token"
}
```

**Response (200 OK):**
```json
{
  "status": "success",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "username": "user123",
    "first_name": "John",
    "last_name": "Doe",
    "profile_picture": "https://...",
    "is_verified": true,
    "role": "user",
    "date_joined": "2024-01-01T00:00:00Z"
  },
  "access_token": "jwt_access_token",
  "refresh_token": "jwt_refresh_token",
  "is_verified": true
}
```

**Cookies Set:**
- `access_token` (HttpOnly, Secure in production)
- `refresh_token` (HttpOnly, Secure in production)

---

#### POST /api/user/auth/google/logout/
**Description:** Logout from Google OAuth and system.

**Headers:**
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body:** None

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Successfully logged out from both system and Google"
}
```

---

#### GET /api/user/social-login-redirect/
**Description:** Redirect after successful social login.

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Request Body:** None

**Response (200 OK):**
```json
{
  "detail": "Successfully authenticated",
  "profile": {
    "id": "uuid",
    "user": {...},
    "bio": "",
    "headline": "John's Profile",
    ...
  }
}
```

---

#### POST /api/user/login/
**Description:** Authenticate user with email and password.

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (200 OK):**
```json
{
  "status": "success",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "username": "user123",
    "first_name": "John",
    "last_name": "Doe",
    "profile_picture": null,
    "is_verified": true,
    "role": "user",
    "date_joined": "2024-01-01T00:00:00Z"
  },
  "profile": {
    "id": "uuid",
    "bio": "",
    "headline": "John's Profile",
    "phone_number": "",
    "location": "",
    ...
  },
  "access_token": "jwt_access_token",
  "refresh_token": "jwt_refresh_token"
}
```

**Response (400 Bad Request):**
```json
{
  "error": "Invalid email or password"
}
```

---

#### POST /api/user/logout/
**Description:** Logout authenticated user.

**Headers:**
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body:** None

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Successfully logged out"
}
```

---

#### GET /api/user/auth/dev-token/
**Description:** Get development token for testing (DEBUG mode only).

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Request Body:** None

**Response (200 OK):**
```json
{
  "access_token": "jwt_access_token",
  "refresh_token": "jwt_refresh_token"
}
```

**Response (403 Forbidden):**
```json
{
  "detail": "This endpoint is only available in development mode"
}
```

---

### User Registration

#### POST /api/user/register/
**Description:** Register a new user account.

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "user@example.com",
  "password": "securePassword123",
  "confirm_password": "securePassword123",
  "role": "user",
  "is_staff": false,
  "is_superuser": false
}
```

**Response (201 Created):**
```json
{
  "status": "success",
  "message": "User registered successfully. Please check your email for verification.",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "username": "johndoe",
    "first_name": "",
    "last_name": "",
    "profile_picture": null,
    "is_verified": false,
    "role": "user",
    "date_joined": "2024-01-01T00:00:00Z"
  },
  "debug": {
    "user_id": "uuid",
    "email": "user@example.com"
  }
}
```

**Response (400 Bad Request):**
```json
{
  "error": "Validation error details"
}
```

---

#### GET /api/user/verify-email/
**Description:** Verify user email address using token.

**Headers:**
```
Content-Type: application/json
```

**Query Parameters:**
- `token` (required): Email verification token

**Request Body:** None

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Email verified successfully",
  "debug": {
    "user_id": "uuid",
    "tokens": {
      "access": "jwt_access_token",
      "refresh": "jwt_refresh_token"
    }
  }
}
```

**Response (400 Bad Request):**
```json
{
  "status": "error",
  "message": "Invalid or expired verification token"
}
```

---

#### POST /api/user/resend-verification-email/
**Description:** Resend verification email to user.

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Verification email has been resent to your email address."
}
```

**Response (500 Internal Server Error):**
```json
{
  "status": "failed",
  "message": "Failed to resend verification email."
}
```

---

### Profile Management

#### GET /api/user/profile/
**Description:** Get current user's profile.

**Headers:**
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body:** None

**Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "profile": {
      "id": "uuid",
      "user": {
        "id": "uuid",
        "email": "user@example.com",
        "username": "johndoe",
        "first_name": "John",
        "last_name": "Doe",
        "profile_picture": null,
        "is_verified": true,
        "role": "user",
        "date_joined": "2024-01-01T00:00:00Z"
      },
      "bio": "Software developer",
      "headline": "Full Stack Developer",
      "phone_number": "+1234567890",
      "location": "New York",
      "birth_date": "1990-01-01",
      "company": "Tech Corp",
      "job_title": "Senior Developer",
      "website": "https://example.com",
      "twitter_url": "https://twitter.com/johndoe",
      "linkedin_url": "https://linkedin.com/in/johndoe",
      "github_url": "https://github.com/johndoe",
      "profile_image": null,
      "profile_image_url": "https://...",
      "cover_image": null,
      "show_email": false,
      "show_phone": false,
      "show_location": true,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z",
      "initials": "JD",
      "image_url": "https://..."
    },
    "meta": {
      "is_complete": true,
      "last_updated": "2024-01-01T00:00:00Z"
    },
    "tokens": {
      "access": "jwt_access_token",
      "refresh": "jwt_refresh_token"
    }
  }
}
```

---

#### PATCH /api/user/profile/
**Description:** Update current user's profile (partial update).

**Headers:**
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "bio": "Updated bio",
  "headline": "Updated headline",
  "phone_number": "+9876543210",
  "location": "San Francisco",
  "company": "New Company",
  "job_title": "Tech Lead",
  "website": "https://newwebsite.com",
  "twitter_url": "https://twitter.com/newhandle",
  "linkedin_url": "https://linkedin.com/in/newprofile",
  "github_url": "https://github.com/newgithub",
  "profile_image": <file>,
  "profile_image_url": "https://newimage.com",
  "show_email": true,
  "show_phone": true,
  "show_location": false
}
```

**Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "id": "uuid",
    "user": {...},
    "bio": "Updated bio",
    "headline": "Updated headline",
    ...
  }
}
```

---

#### PUT /api/user/profile/
**Description:** Update current user's profile (full update).

**Headers:**
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body:** Same as PATCH but all fields required

**Response (200 OK):** Same as PATCH

---

#### DELETE /api/user/profile/
**Description:** Delete current user's profile.

**Headers:**
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body:** None

**Response (204 No Content):**
```json
{
  "status": "success",
  "message": "Profile deleted successfully."
}
```

---

#### GET /api/user/account-info/
**Description:** Get current user's account information.

**Headers:**
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body:** None

**Response (200 OK):**
```json
{
  "id": "uuid",
  "username": "johndoe",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "user",
  "is_staff": false,
  "is_superuser": false,
  "is_active": true,
  "is_verified": true,
  "date_joined": "2024-01-01T00:00:00Z"
}
```

---

### Password Management

#### POST /api/user/request-password-reset/
**Description:** Request password reset email.

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Password reset link has been sent to your email."
}
```

---

#### POST /api/user/validate-reset-token/
**Description:** Validate password reset token.

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "token": "reset_token_string",
  "userId": "uuid"
}
```

**Response (200 OK):**
```json
{
  "status": "successful",
  "message": "Reset verification successful",
  "token": "reset_token_string",
  "userId": "uuid"
}
```

**Response (400 Bad Request):**
```json
{
  "detail": "Invalid or expired reset token"
}
```

---

#### POST /api/user/reset-password/
**Description:** Reset password with valid token.

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "token": "reset_token_string",
  "newPassword": "newSecurePassword123",
  "confirmNewPassword": "newSecurePassword123",
  "userId": "uuid"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Password reset successfully. You may login with your new password"
}
```

---

#### PUT /api/user/change-password/
**Description:** Change password for authenticated user.

**Headers:**
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "currentPassword": "oldPassword123",
  "newPassword": "newSecurePassword123",
  "confirmNewPassword": "newSecurePassword123"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Password changed successfully"
}
```

**Response (400 Bad Request):**
```json
{
  "error": "Current password is incorrect"
}
```

---

### User Management (Admin)

#### DELETE /api/user/delete-account/
**Description:** Delete current user's account and all associated data.

**Headers:**
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body:** None

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Account and all associated data deleted successfully",
  "deletion_report": {
    "deleted_user": "uuid",
    "deleted_profile": "uuid",
    "deleted_contacts": 5,
    "deleted_newsletters": 2
  },
  "metadata": {
    "timestamp": "2024-01-01T00:00:00Z",
    "deletion_complete": true
  }
}
```

---

#### DELETE /api/user/delete-all-except-admin/
**Description:** Delete all users except admin users (Admin only).

**Headers:**
```
Authorization: Bearer <admin_jwt_token>
Content-Type: application/json
```

**Request Body:** None

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "15 user(s) (excluding admins) deleted successfully."
}
```

---

#### DELETE /api/user/delete/<uuid:userId>/
**Description:** Delete a specific user by ID (Admin only).

**Headers:**
```
Authorization: Bearer <admin_jwt_token>
Content-Type: application/json
```

**URL Parameters:**
- `userId` (required): UUID of the user to delete

**Request Body:** None

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "User with ID uuid and associated data deleted successfully.",
  "deletion_report": {
    "deleted_user": "uuid",
    "deleted_profile": "uuid",
    "deleted_contacts": 3
  }
}
```

**Response (404 Not Found):**
```json
{
  "error": "User with ID uuid not found."
}
```

---

#### DELETE /api/user/delete-unverified/
**Description:** Delete all unverified users (Admin only).

**Headers:**
```
Authorization: Bearer <admin_jwt_token>
Content-Type: application/json
```

**Request Body:** None

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "8 unverified user(s) deleted successfully."
}
```

---

#### PUT /api/user/update-role/<uuid:user_id>/
**Description:** Update user role and permissions (Admin only).

**Headers:**
```
Authorization: Bearer <admin_jwt_token>
Content-Type: application/json
```

**URL Parameters:**
- `user_id` (required): UUID of the user to update

**Request Body:**
```json
{
  "role": "admin",
  "is_staff": true,
  "is_superuser": false
}
```

**Response (200 OK):**
```json
{
  "status": "success",
  "user_id": "uuid",
  "new_role": "admin",
  "is_staff": true,
  "is_superuser": false
}
```

**Response (403 Forbidden):**
```json
{
  "detail": "You do not have permission to perform this action"
}
```

**Response (404 Not Found):**
```json
{
  "detail": "User not found"
}
```

---

#### GET /api/user/users/<uuid:userId>/
**Description:** Get a specific user by ID (Admin only).

**Headers:**
```
Authorization: Bearer <admin_jwt_token>
Content-Type: application/json
```

**URL Parameters:**
- `userId` (required): UUID of the user to retrieve

**Request Body:** None

**Response (200 OK):**
```json
{
  "id": "uuid",
  "username": "johndoe",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "user",
  "is_staff": false,
  "is_superuser": false,
  "is_active": true,
  "is_verified": true,
  "date_joined": "2024-01-01T00:00:00Z"
}
```

**Response (404 Not Found):**
```json
{
  "error": "User with ID uuid not found."
}
```

---

#### GET /api/user/users/
**Description:** Get all users (Admin only).

**Headers:**
```
Authorization: Bearer <admin_jwt_token>
Content-Type: application/json
```

**Request Body:** None

**Response (200 OK):**
```json
[
  {
    "id": "uuid",
    "username": "johndoe",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "user",
    "is_staff": false,
    "is_superuser": false,
    "is_active": true,
    "is_verified": true,
    "date_joined": "2024-01-01T00:00:00Z"
  },
  ...
]
```

---

### Health Check

#### GET /api/user/health/
**Description:** Health check endpoint for monitoring.

**Headers:** None required

**Request Body:** None

**Response (200 OK):**
```json
{
  "status": "ok"
}
```

---

## Contact App Endpoints

### Contact Form

#### POST /api/contacts/create/
**Description:** Create a new contact submission.

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "John Doe",
  "phone": "+1234567890",
  "email": "contact@example.com",
  "subject": "Project Inquiry",
  "message": "I would like to discuss a project with you."
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "name": "John Doe",
  "phone": "+1234567890",
  "email": "contact@example.com",
  "subject": "Project Inquiry",
  "message": "I would like to discuss a project with you.",
  "created_at": "2024-01-01T00:00:00Z",
  "is_read": false
}
```

**Response (400 Bad Request):**
```json
{
  "error": "Validation error details"
}
```

---

#### GET /api/contacts/
**Description:** Get all contact submissions (Admin only).

**Headers:**
```
Authorization: Bearer <admin_jwt_token>
Content-Type: application/json
```

**Request Body:** None

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "phone": "+1234567890",
    "email": "contact@example.com",
    "subject": "Project Inquiry",
    "message": "I would like to discuss a project with you.",
    "created_at": "2024-01-01T00:00:00Z",
    "is_read": false
  },
  ...
]
```

---

#### GET /api/contacts/<int:pk>/
**Description:** Get a specific contact submission by ID (Admin only).

**Headers:**
```
Authorization: Bearer <admin_jwt_token>
Content-Type: application/json
```

**URL Parameters:**
- `pk` (required): Primary key of the contact submission

**Request Body:** None

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "John Doe",
  "phone": "+1234567890",
  "email": "contact@example.com",
  "subject": "Project Inquiry",
  "message": "I would like to discuss a project with you.",
  "created_at": "2024-01-01T00:00:00Z",
  "is_read": false
}
```

---

#### PATCH /api/contacts/<int:pk>/update/
**Description:** Update a contact submission (Admin only).

**Headers:**
```
Authorization: Bearer <admin_jwt_token>
Content-Type: application/json
```

**URL Parameters:**
- `pk` (required): Primary key of the contact submission

**Request Body:**
```json
{
  "name": "Updated Name",
  "subject": "Updated Subject",
  "is_read": true
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "Updated Name",
  "phone": "+1234567890",
  "email": "contact@example.com",
  "subject": "Updated Subject",
  "message": "I would like to discuss a project with you.",
  "created_at": "2024-01-01T00:00:00Z",
  "is_read": true
}
```

---

#### DELETE /api/contacts/<int:pk>/delete/
**Description:** Delete a contact submission (Admin only).

**Headers:**
```
Authorization: Bearer <admin_jwt_token>
Content-Type: application/json
```

**URL Parameters:**
- `pk` (required): Primary key of the contact submission

**Request Body:** None

**Response (204 No Content)**

---

### Newsletter Management

#### POST /api/newsletter/subscribe/
**Description:** Subscribe to newsletter.

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "email": "subscriber@example.com"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "email": "subscriber@example.com",
  "subscribed_at": "2024-01-01T00:00:00Z",
  "is_active": true
}
```

**Response (400 Bad Request):**
```json
{
  "email": ["This email is already subscribed."]
}
```

---

#### GET /api/newsletter/unsubscribe/
**Description:** Unsubscribe from newsletter (for clickable links).

**Headers:** None required

**Query Parameters:**
- `email` (required): Email to unsubscribe

**Request Body:** None

**Response (200 OK):**
```json
{
  "message": "Successfully unsubscribed from newsletter"
}
```

---

#### POST /api/newsletter/unsubscribe/
**Description:** Unsubscribe from newsletter (for API requests).

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "email": "subscriber@example.com"
}
```

**Response (200 OK):**
```json
{
  "message": "Successfully unsubscribed from newsletter"
}
```

---

#### GET /api/newsletter/subscribers/
**Description:** Get all active newsletter subscribers (Admin only).

**Headers:**
```
Authorization: Bearer <admin_jwt_token>
Content-Type: application/json
```

**Request Body:** None

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "email": "subscriber@example.com",
    "subscribed_at": "2024-01-01T00:00:00Z",
    "is_active": true
  },
  ...
]
```

---

#### GET /api/newsletter/subscribers/<int:pk>/
**Description:** Get a specific newsletter subscriber (Admin only).

**Headers:**
```
Authorization: Bearer <admin_jwt_token>
Content-Type: application/json
```

**URL Parameters:**
- `pk` (required): Primary key of the subscriber

**Request Body:** None

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "subscriber@example.com",
  "subscribed_at": "2024-01-01T00:00:00Z",
  "is_active": true
}
```

---

#### PATCH /api/newsletter/subscribers/<int:pk>/update/
**Description:** Update newsletter subscriber (Admin only).

**Headers:**
```
Authorization: Bearer <admin_jwt_token>
Content-Type: application/json
```

**URL Parameters:**
- `pk` (required): Primary key of the subscriber

**Request Body:**
```json
{
  "email": "updated@example.com"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "updated@example.com",
  "subscribed_at": "2024-01-01T00:00:00Z",
  "is_active": true
}
```

**Response (400 Bad Request):**
```json
{
  "error": "Use the unsubscribe endpoint for deactivating subscribers."
}
```

---

#### DELETE /api/newsletter/subscribers/<int:pk>/delete/
**Description:** Delete newsletter subscriber (Admin only).

**Headers:**
```
Authorization: Bearer <admin_jwt_token>
Content-Type: application/json
```

**URL Parameters:**
- `pk` (required): Primary key of the subscriber

**Request Body:** None

**Response (204 No Content)**

---

### Deleted Subscribers (Admin Only)

#### GET /api/newsletter/deleted/
**Description:** Get all deleted subscribers (Admin only).

**Headers:**
```
Authorization: Bearer <admin_jwt_token>
Content-Type: application/json
```

**Request Body:** None

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "email": "deleted@example.com",
    "unsubscribed_at": "2024-01-01T00:00:00Z",
    "deleted_at": "2024-01-01T00:00:00Z"
  },
  ...
]
```

---

#### GET /api/newsletter/deleted/<int:pk>/
**Description:** Get a specific deleted subscriber (Admin only).

**Headers:**
```
Authorization: Bearer <admin_jwt_token>
Content-Type: application/json
```

**URL Parameters:**
- `pk` (required): Primary key of the deleted subscriber

**Request Body:** None

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "deleted@example.com",
  "unsubscribed_at": "2024-01-01T00:00:00Z",
  "deleted_at": "2024-01-01T00:00:00Z"
}
```

---

#### DELETE /api/newsletter/deleted/<int:pk>/delete/
**Description:** Permanently delete a deleted subscriber record (Admin only).

**Headers:**
```
Authorization: Bearer <admin_jwt_token>
Content-Type: application/json
```

**URL Parameters:**
- `pk` (required): Primary key of the deleted subscriber

**Request Body:** None

**Response (204 No Content)**

---

#### DELETE /api/newsletter/deleted/clear-all/
**Description:** Clear all deleted subscribers (Admin only).

**Headers:**
```
Authorization: Bearer <admin_jwt_token>
Content-Type: application/json
```

**Request Body:** None

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "All deleted subscribers cleared successfully",
  "deleted_count": 10
}
```

---

#### POST /api/newsletter/deleted/reactivate/
**Description:** Reactivate a deleted subscriber (Admin only).

**Headers:**
```
Authorization: Bearer <admin_jwt_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "email": "deleted@example.com"
}
```

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Subscriber reactivated successfully",
  "subscriber": {
    "id": 1,
    "email": "deleted@example.com",
    "subscribed_at": "2024-01-01T00:00:00Z",
    "is_active": true
  }
}
```

**Response (400 Bad Request):**
```json
{
  "error": "Subscriber not found in deleted list or already active"
}
```

---

## Missing Endpoints & Implementation Notes

### User Account App

#### 1. Microsoft OAuth Login Endpoint
**Status:** ✅ IMPLEMENTED (MicrosoftLogin class exists but no URL route)

**Implementation Note:** The `MicrosoftLogin` class exists in `views.py` but is not routed in `users_urls.py`. To implement:

```python
# Add to users_urls.py
path("auth/microsoft/", MicrosoftLogin.as_view(), name="microsoft_login"),
```

**Expected Endpoint:** `POST /api/user/auth/microsoft/`

---

#### 2. Switch Account Endpoint
**Status:** ✅ IMPLEMENTED (SwitchAccountView class exists but no URL route)

**Implementation Note:** The `SwitchAccountView` class exists in `views.py` but is not routed in `users_urls.py`. To implement:

```python
# Add to users_urls.py
path("switch-account/", SwitchAccountView.as_view(), name="switch-account"),
```

**Expected Endpoint:** `GET /api/user/switch-account/`

---

#### 3. User Search/Filter Endpoint
**Status:** ❌ NOT IMPLEMENTED

**Implementation Note:** No endpoint exists for searching or filtering users. Recommended implementation:

```python
# Add to users_urls.py
path("users/search/", UserSearchView.as_view(), name="user-search"),

# Add to views.py
class UserSearchView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrSuperUser]
    
    def get(self, request):
        query = request.query_params.get('q', '')
        role = request.query_params.get('role', '')
        is_verified = request.query_params.get('is_verified', '')
        
        users = CustomUser.objects.all()
        
        if query:
            users = users.filter(
                Q(email__icontains=query) | 
                Q(username__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            )
        
        if role:
            users = users.filter(role=role)
            
        if is_verified:
            users = users.filter(is_verified=is_verified.lower() == 'true')
        
        serializer = UserDetailSerializer(users, many=True)
        return Response(serializer.data)
```

**Expected Endpoint:** `GET /api/user/users/search/?q=john&role=user&is_verified=true`

---

#### 4. Bulk User Operations Endpoint
**Status:** ❌ NOT IMPLEMENTED

**Implementation Note:** No endpoint exists for bulk user operations (e.g., bulk update roles, bulk delete). Recommended implementation:

```python
# Add to users_urls.py
path("users/bulk/", BulkUserOperationsView.as_view(), name="bulk-user-operations"),

# Add to views.py
class BulkUserOperationsView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrSuperUser]
    
    def post(self, request):
        operation = request.data.get('operation')  # 'delete', 'update_role', 'verify'
        user_ids = request.data.get('user_ids', [])
        
        if operation == 'delete':
            deleted_count = AdminUserDeletionService.bulk_delete_users(user_ids)
            return Response({"status": "success", "deleted_count": deleted_count})
        
        elif operation == 'update_role':
            new_role = request.data.get('role')
            updated_count = AdminUserManagementService.bulk_update_roles(user_ids, new_role)
            return Response({"status": "success", "updated_count": updated_count})
        
        elif operation == 'verify':
            verified_count = UserService.bulk_verify_users(user_ids)
            return Response({"status": "success", "verified_count": verified_count})
```

**Expected Endpoint:** `POST /api/user/users/bulk/`

---

#### 5. User Statistics/Analytics Endpoint
**Status:** ❌ NOT IMPLEMENTED

**Implementation Note:** No endpoint exists for user statistics. Recommended implementation:

```python
# Add to users_urls.py
path("users/statistics/", UserStatisticsView.as_view(), name="user-statistics"),

# Add to views.py
class UserStatisticsView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrSuperUser]
    
    def get(self, request):
        total_users = CustomUser.objects.count()
        verified_users = CustomUser.objects.filter(is_verified=True).count()
        unverified_users = total_users - verified_users
        
        role_stats = {}
        for role in UserRole:
            role_stats[role.value] = CustomUser.objects.filter(role=role.value).count()
        
        recent_users = CustomUser.objects.order_by('-date_joined')[:10]
        recent_serializer = UserDetailSerializer(recent_users, many=True)
        
        return Response({
            "total_users": total_users,
            "verified_users": verified_users,
            "unverified_users": unverified_users,
            "role_distribution": role_stats,
            "recent_users": recent_serializer.data
        })
```

**Expected Endpoint:** `GET /api/user/users/statistics/`

---

#### 6. Profile Image Upload Endpoint
**Status:** ✅ FULLY IMPLEMENTED

**Implementation Note:** Dedicated profile image upload endpoint has been successfully implemented with file validation (type and size limits).

**Endpoint:** `POST /api/user/profile/upload-image/`

**Headers:**
```
Authorization: Bearer <jwt_token>
Content-Type: multipart/form-data
```

**Request Body:**
```
image: <file> (multipart/form-data)
```

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Profile image uploaded successfully",
  "data": {
    "id": "uuid",
    "user": {...},
    "profile_image": "/media/profile_images/image.jpg",
    "profile_image_url": "",
    ...
  }
}
```

**Response (400 Bad Request):**
```json
{
  "error": "No image file provided"
}
```

```json
{
  "error": "File must be an image"
}
```

```json
{
  "error": "File size exceeds 5MB limit"
}
```

---

### Contact App

#### 1. Contact Search/Filter Endpoint
**Status:** ⚠️ PARTIALLY IMPLEMENTED

**Implementation Note:** The ContactSearchView has been implemented in `contact/views.py` but needs to be added to `contact/urls.py` to be accessible.

**To Complete Implementation:**
Add this line to `contact/urls.py` in the urlpatterns list:
```python
path('contacts/search/', ContactSearchView.as_view(), name='contact-search'),
```

Also add to imports:
```python
from .views import (
    ...,
    ContactSearchView,
)
```

**Expected Endpoint:** `GET /api/contacts/search/?q=john&is_read=false&date_from=2024-01-01`

**Headers:**
```
Authorization: Bearer <admin_jwt_token>
```

**Query Parameters:**
- `q` (optional): Search query for name, email, or subject
- `is_read` (optional): Filter by read status (true/false)
- `date_from` (optional): Filter contacts from this date
- `date_to` (optional): Filter contacts until this date

**Response (200 OK):**
```json
{
  "status": "success",
  "count": 5,
  "data": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "subject": "Project Inquiry",
      ...
    }
  ]
}
```

---

#### 2. Bulk Contact Operations Endpoint
**Status:** ❌ NOT IMPLEMENTED

**Implementation Note:** No endpoint exists for bulk contact operations (e.g., mark as read, bulk delete). Recommended implementation:

```python
# Add to urls.py
path('contacts/bulk/', BulkContactOperationsView.as_view(), name='bulk-contact-operations'),

# Add to views.py
class BulkContactOperationsView(APIView):
    permission_classes = [IsAdminOrSuperUser]
    
    def post(self, request):
        operation = request.data.get('operation')  # 'mark_read', 'mark_unread', 'delete'
        contact_ids = request.data.get('contact_ids', [])
        
        if operation == 'mark_read':
            Contact.objects.filter(id__in=contact_ids).update(is_read=True)
            return Response({"status": "success", "message": f"Marked {len(contact_ids)} contacts as read"})
        
        elif operation == 'mark_unread':
            Contact.objects.filter(id__in=contact_ids).update(is_read=False)
            return Response({"status": "success", "message": f"Marked {len(contact_ids)} contacts as unread"})
        
        elif operation == 'delete':
            deleted_count = Contact.objects.filter(id__in=contact_ids).delete()[0]
            return Response({"status": "success", "message": f"Deleted {deleted_count} contacts"})
```

**Expected Endpoint:** `POST /api/contacts/bulk/`

---

#### 3. Contact Statistics Endpoint
**Status:** ⚠️ PARTIALLY IMPLEMENTED

**Implementation Note:** The ContactStatisticsView has been implemented in `contact/views.py` but needs to be added to `contact/urls.py` to be accessible.

**To Complete Implementation:**
Add this line to `contact/urls.py` in the urlpatterns list:
```python
path('contacts/statistics/', ContactStatisticsView.as_view(), name='contact-statistics'),
```

Also add to imports:
```python
from .views import (
    ...,
    ContactStatisticsView,
)
```

**Expected Endpoint:** `GET /api/contacts/statistics/`

**Headers:**
```
Authorization: Bearer <admin_jwt_token>
```

**Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "total_contacts": 25,
    "unread_contacts": 10,
    "read_contacts": 15,
    "recent_contacts_30_days": 8,
    "recent_contacts_7_days": 3
  }
}
```

---

#### 4. Newsletter Campaign Management Endpoint
**Status:** ⚠️ PARTIALLY IMPLEMENTED

**Implementation Note:** The NewsletterCampaign model has been created in `contact/models.py` with comprehensive fields for campaign management. However, the serializer, views, and URL routes still need to be implemented.

**To Complete Implementation:**

1. **Add Serializer to `contact/serializers.py`:**
```python
class NewsletterCampaignSerializer(serializers.ModelSerializer):
    created_by_email = serializers.SerializerMethodField()

    class Meta:
        model = NewsletterCampaign
        fields = [
            'id', 'title', 'subject', 'content', 'status',
            'scheduled_for', 'sent_at', 'created_at', 'updated_at',
            'created_by', 'created_by_email', 'recipient_count',
            'opened_count', 'clicked_count'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at', 'sent_at',
            'created_by', 'recipient_count', 'opened_count', 'clicked_count'
        ]

    def get_created_by_email(self, obj):
        if obj.created_by:
            return obj.created_by.email
        return None
```

2. **Create Views in `contact/views.py`:**
```python
class NewsletterCampaignListView(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrSuperUser]
    serializer_class = NewsletterCampaignSerializer
    queryset = NewsletterCampaign.objects.all()

class NewsletterCampaignDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrSuperUser]
    serializer_class = NewsletterCampaignSerializer
    queryset = NewsletterCampaign.objects.all()
```

3. **Add URL Routes to `contact/urls.py`:**
```python
path('newsletter/campaigns/', NewsletterCampaignListView.as_view(), name='newsletter-campaigns'),
path('newsletter/campaigns/<int:pk>/', NewsletterCampaignDetailView.as_view(), name='newsletter-campaign-detail'),
```

**Expected Endpoints:**
- `POST /api/newsletter/campaigns/` - Create campaign
- `GET /api/newsletter/campaigns/` - List campaigns
- `GET /api/newsletter/campaigns/<int:pk>/` - Get campaign details
- `PUT /api/newsletter/campaigns/<int:pk>/` - Update campaign
- `DELETE /api/newsletter/campaigns/<int:pk>/` - Delete campaign

---

#### 5. Email Template Management Endpoint
**Status:** ❌ NOT IMPLEMENTED

**Implementation Note:** No endpoint exists for managing email templates. This would be useful for customizing contact form responses and newsletter templates.

```python
# New model needed
class EmailTemplate(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subject = models.CharField(max_length=200)
    body = models.TextField()
    is_active = models.BooleanField(default=True)

# Add to urls.py
path('email-templates/', EmailTemplateListView.as_view(), name='email-templates'),
path('email-templates/<int:pk>/', EmailTemplateDetailView.as_view(), name='email-template-detail'),
```

**Expected Endpoints:**
- `GET /api/email-templates/` - List email templates
- `POST /api/email-templates/` - Create email template
- `GET /api/email-templates/<int:pk>/` - Get template details
- `PUT /api/email-templates/<int:pk>/` - Update template
- `DELETE /api/email-templates/<int:pk>/` - Delete template

---

## Common Response Codes

- **200 OK** - Request successful
- **201 Created** - Resource created successfully
- **204 No Content** - Request successful, no content returned
- **400 Bad Request** - Invalid request data
- **401 Unauthorized** - Authentication required
- **403 Forbidden** - Insufficient permissions
- **404 Not Found** - Resource not found
- **500 Internal Server Error** - Server error

## Authentication

Most endpoints require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

Tokens can be obtained via:
- `/api/user/login/` - Email/password login
- `/api/user/auth/google/` - Google OAuth login
- `/api/user/verify-email/` - Returns tokens after email verification

## Rate Limiting

The API implements rate limiting:
- **Anonymous users:** 10,000 requests per hour
- **Authenticated users:** 100,000 requests per hour

## Pagination

List endpoints support pagination with default page size of 20 items. Use query parameters:
- `page` - Page number
- `page_size` - Items per page

## Error Handling

All endpoints return consistent error responses:

```json
{
  "status": "error",
  "code": "error_code",
  "message": "Human readable error message",
  "details": {...}
}
```

---

## Implementation Summary (June 18, 2026)

### ✅ Fully Implemented Endpoints

1. **Profile Image Upload** - `POST /api/user/profile/upload-image/`
   - View: `ProfileImageUploadView` in `user_account/views.py`
   - URL: Added to `user_account/users_urls.py`
   - Features: File validation (type and size), automatic old image deletion

### ⚠️ Partially Implemented Endpoints (Need URL Routes)

2. **Contact Search/Filter** - `GET /api/contacts/search/`
   - View: `ContactSearchView` in `contact/views.py`
   - Missing: URL route in `contact/urls.py`
   - Features: Search by name/email/subject, filter by read status, date range filtering

3. **Contact Statistics** - `GET /api/contacts/statistics/`
   - View: `ContactStatisticsView` in `contact/views.py`
   - Missing: URL route in `contact/urls.py`
   - Features: Total/read/unread counts, recent contacts (7/30 days)

### ⚠️ Partially Implemented Endpoints (Need Serializer + Views + URLs)

4. **Newsletter Campaign Management**
   - Model: `NewsletterCampaign` in `contact/models.py`
   - Missing: Serializer, views, and URL routes
   - Features: Campaign creation, scheduling, tracking (opened/clicked counts)

### 🔧 Quick Fix Instructions

To enable the partially implemented Contact endpoints, add these lines to `contact/urls.py`:

**In imports section:**
```python
from .views import (
    ...,
    ContactSearchView,
    ContactStatisticsView,
)
```

**In urlpatterns list:**
```python
path('contacts/search/', ContactSearchView.as_view(), name='contact-search'),
path('contacts/statistics/', ContactStatisticsView.as_view(), name='contact-statistics'),
```

**Note:** Don't forget to run migrations after adding the NewsletterCampaign model:
```bash
python manage.py makemigrations contact
python manage.py migrate
```

---

**Document Version:** 1.1.0
**Last Updated:** June 18, 2026
**API Version:** 1.0.0
