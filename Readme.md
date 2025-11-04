<div align="center">

# 🌐 SocialX Web

### *A Modern Social Media Platform Built with Django*

[![Django](https://img.shields.io/badge/Django-5.2.7-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

[🚀 Live Demo](https://socialxweb.pythonanywhere.com) • [📖 Documentation](#installation) • [🐛 Report Bug](https://github.com/YOUR_USERNAME/SocialX-Web/issues) • [✨ Request Feature](https://github.com/YOUR_USERNAME/SocialX-Web/issues)

*Connect. Share. Inspire. Express yourself with the world.*

---

### 🌟 [**Try Live Demo →**](https://socialxweb.pythonanywhere.com)

</div>

---

## 📋 Table of Contents

- [About The Project](#-about-the-project)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
- [Installation](#-installation)
- [Email Configuration](#-email-configuration)
- [Mobile Access](#-mobile-access)
- [Project Structure](#-project-structure)
- [Security Features](#-security-features)
- [API Endpoints](#-api-endpoints)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)
- [Acknowledgments](#-acknowledgments)

---

## 🎯 About The Project

**SocialX Web** is a full-featured social media platform that allows users to connect, share content, and engage with a vibrant community. Built with Django and modern web technologies, it offers a seamless experience across all devices.

### 🎨 What Makes It Special?

- ⚡ **Real-time Interactions** - AJAX-powered likes and saves without page reloads
- 🔐 **Secure Authentication** - Email verification with time-limited OTP codes
- 📱 **Fully Responsive** - Perfect experience on desktop, tablet, and mobile
- 🌓 **Dark Mode** - Easy on the eyes, day or night
- 📧 **Professional Emails** - Beautiful HTML email templates via Gmail SMTP
- 🎥 **Rich Media Support** - Share images and videos up to 100MB
- 🔒 **Privacy Controls** - Private accounts and download restrictions

---

## ✨ Key Features

### 🔐 Authentication & Security

- ✅ **Email Verification System**
  - 6-digit OTP codes sent via email
  - 10-minute expiration for security
  - Beautiful HTML email templates
  - Gmail SMTP integration

- ✅ **Advanced Username Validation**
  - Must start with a letter (a-z, A-Z)
  - Supports letters, numbers, dots (.), and underscores (_)
  - No special characters or spaces
  - Unique username enforcement

- ✅ **Secure Password System**
  - PBKDF2 hashing algorithm
  - Minimum length requirements
  - Common password validation
  - Password strength indicators

- ✅ **Account Management**
  - Change username with real-time validation
  - Change email with OTP verification
  - Account deletion with double confirmation
  - Session management

### 📱 Social Features

- ✅ **Posts & Content**
  - Create text posts (up to 280 characters)
  - Upload images (JPG, PNG, GIF)
  - Upload videos (MP4, WebM) up to 100MB
  - Edit and delete your posts
  - Post timestamps with "time ago" format

- ✅ **Engagement System**
  - Like posts with instant feedback (AJAX)
  - Save/bookmark posts for later
  - Comment on posts
  - View engagement counts in real-time

- ✅ **Social Networking**
  - Follow/unfollow users
  - See follower and following counts
  - Discover other users through search
  - View user profiles with post history

- ✅ **Notifications**
  - Get notified when someone likes your post
  - Notification for new comments
  - Follow notifications
  - Mark all as read functionality
  - Unread notification badges

- ✅ **Search Functionality**
  - Search for users by username
  - Search posts by content
  - Real-time search results
  - Highlighted search terms

### 👤 Profile Management

- ✅ **Customizable Profiles**
  - Upload custom profile pictures
  - Write personal bio
  - Display full name (optional)
  - Profile statistics (posts, followers, following)

- ✅ **Privacy Settings**
  - Private account mode
  - Restrict media downloads to account owner
  - Control who can see your content
  - Manage followers

- ✅ **Profile Updates**
  - Edit profile information
  - Change username (with validation)
  - Change email (with OTP verification)
  - Update profile picture and bio

### 🎨 User Experience

- ✅ **Modern UI/UX**
  - Clean, intuitive interface
  - Smooth animations and transitions
  - Professional color scheme
  - Consistent design language

- ✅ **Dark/Light Mode**
  - Toggle between themes instantly
  - Preference saved in browser
  - Smooth color transitions
  - Optimized for readability

- ✅ **Responsive Design**
  - Mobile-first approach
  - Works on all screen sizes
  - Touch-friendly interfaces
  - Optimized images and videos

- ✅ **Performance**
  - AJAX for instant interactions
  - Lazy loading for images
  - Optimized database queries
  - Fast page load times
  - Scroll position preservation

### 📧 Email System

- ✅ **Professional Email Templates**
  - Beautiful HTML designs
  - Gradient headers
  - Responsive email layout
  - Clear call-to-action buttons

- ✅ **Email Features**
  - Registration verification
  - Email change verification
  - Password reset (future feature)
  - Welcome emails
  - Notification emails (future feature)

---

## 🛠 Tech Stack

### Backend
- **Framework:** Django 5.2.7
- **Language:** Python 3.11
- **Database:** SQLite (Development) / PostgreSQL (Production Ready)
- **Authentication:** Django Auth System
- **Email:** Gmail SMTP

### Frontend
- **CSS Framework:** Bootstrap 5.3.3
- **Icons:** Bootstrap Icons
- **JavaScript:** Vanilla JS (AJAX)
- **Templates:** Django Template Language

### Deployment
- **Platform:** PythonAnywhere
- **Web Server:** WSGI
- **Static Files:** WhiteNoise (Production Ready)
- **Version Control:** Git & GitHub

### Development Tools
- **Environment:** python-dotenv
- **Image Processing:** Pillow
- **Package Manager:** pip
- **Virtual Environment:** venv

---

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11 or higher** - [Download](https://www.python.org/downloads/)
- **pip** - Usually comes with Python
- **Git** - [Download](https://git-scm.com/downloads)
- **Virtual Environment** (recommended)

### Quick Start

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/SocialX-Web.git

# Navigate to project directory
cd SocialX-Web

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Navigate to project root
cd socialx

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

🤝 Contributing
Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated!

How to Contribute
Fork the Project

Bash

# Click the 'Fork' button at the top right of this page
Clone Your Fork

Bash

git clone https://github.com/YOUR_USERNAME/SocialX-Web.git
cd SocialX-Web
Create a Feature Branch

Bash

git checkout -b feature/AmazingFeature
Make Your Changes

Write clean, commented code
Follow Django best practices
Test your changes thoroughly
Commit Your Changes

Bash

git add .
git commit -m "Add some AmazingFeature"
Push to Your Fork

Bash

git push origin feature/AmazingFeature
Open a Pull Request

Go to the original repository
Click "New Pull Request"
Describe your changes
Code of Conduct
Please be respectful and constructive in all interactions. We aim to foster an inclusive and welcoming community.

📄 License
Distributed under the MIT License. See LICENSE file for more information.

text

MIT License

Copyright (c) 2025 SocialX Web

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
📞 Contact
Project Maintainer: Your Name

🌐 Portfolio: codebynilesh.pythonanywhere.com
📧 Email: socialxweb.official@gmail.com
💼 GitHub: @YOUR_USERNAME
🔗 LinkedIn: Your LinkedIn
Project Link: https://github.com/YOUR_USERNAME/SocialX-Web

Live Demo: https://socialxweb.pythonanywhere.com

🙏 Acknowledgments
Special thanks to these amazing resources and tools:

Django - The web framework for perfectionists with deadlines
Bootstrap - For the beautiful, responsive UI components
Bootstrap Icons - For the comprehensive icon library
PythonAnywhere - For reliable, easy Python hosting
Gmail SMTP - For professional email delivery
Python - For being an amazing programming language
MDN Web Docs - For comprehensive web development documentation
Stack Overflow - For the developer community support
Inspiration
This project was inspired by modern social media platforms while focusing on:

Simplicity - Easy to use, easy to understand
Security - User data protection as a priority
Performance - Fast and responsive experience
Privacy - User control over their data


🗺️ Roadmap
Version 0.1.0 (Upcoming)
 Direct messaging system
 Real-time chat with WebSockets
 Stories feature (24-hour posts)
 Hashtag support and trending topics
 Mention users in posts (@username)
 Post sharing/reposting
Version 0.2.0 (Future)
 Advanced search with filters
 Infinite scroll pagination
 Video compression for large files
 Image editing before upload
 Multiple image uploads per post
 Dark mode custom themes
Version 1.0.0 (Long-term)
 Mobile app (React Native)
 Progressive Web App (PWA)
 Video calls integration
 Live streaming
 Monetization features
 Analytics dashboard
See the open issues for a full list of proposed features and known issues.

⭐ Support
If you found this project helpful, please consider:

⭐ Starring this repository - It helps others discover the project
🐛 Reporting bugs - Help us improve by reporting issues
💡 Suggesting features - Share your ideas for new features
🔀 Forking and contributing - Make the project even
