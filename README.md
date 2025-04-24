# 📝 Flask Blog Website

A feature-rich **blog platform built with Flask**, offering secure user authentication, comment systems, admin controls, and a clean, modern design with Gravatar avatars. Ideal for learning full-stack development using Python.

---

## 🚀 Features

### 🔐 User Authentication
- Register and login using **Flask-WTF** forms
- Passwords are securely hashed using `werkzeug.security`
- Logged-in session management with **Flask-Login**

### 🧑‍💻 User Profiles & Gravatars
- Gravatar integration for user avatars
- Custom helper used for Gravatar compatibility with **Flask 2.3+**

### 📝 Blog Posts
- Admin can **create**, **edit**, and **delete** blog posts
- Posts include **title**, **subtitle**, **image**, **publish date**, and **rich text content**

### 💬 Comment System
- Logged-in users can comment on blog posts
- Each comment is linked to the user and the post via one-to-many relationships

### 🧠 Admin Control
- Only admin users can create or delete posts
- Admin-only routes protected using a custom `@admin_only` decorator

### 🖋️ Rich Text Editor
- Integrated **Flask-CKEditor** for both blog and comment content
- Clean and markdown-style formatting support

### 💾 Database
- Uses **SQLite** with **SQLAlchemy ORM**
- Database Models:
  - `UserData`
  - `BlogPost`
  - `Comment`
- Relationships:
  - One-to-many: `UserData` → `BlogPost`
  - One-to-many: `BlogPost` → `Comment`
  - One-to-many: `UserData` → `Comment`

### 🔒 Admin Protection
- Routes like `/create`, `/edit`, and `/delete` are restricted to admins only using a custom `@admin_only` decorator
- Admin identity based on first registered user or specific condition

---

## 💡 Future Improvements

- 👍 Like/Dislike system for posts and comments  
- 📄 Pagination for blog and comment sections  
- 📝 Markdown rendering support  
- ✉️ Email verification & password reset  
- 📊 Admin dashboard with insights

---

## 📦 Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/Flask-Blog-Website.git
   cd Flask-Blog-Website
   pip install -r requirements.txt
   python app.py

---

## 🧑‍💻 Author

### Soumik Pakhira
Flask Developer | Django Developer | Python Enthusiast
🔗 www.linkedin.com/in/soumikpakhira




  
