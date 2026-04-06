# 🍔 VYRA — Food Ordering Tracking System

<h1 align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=28&duration=3000&pause=1000&color=FF6B6B&center=true&width=600&lines=🍔+VYRA+Food+Order+Tracker;Track+Orders+in+Real+Time;Built+with+Flask+%26+MySQL" alt="Typing animation" />
</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Flask-2.0+-green.svg?style=for-the-badge&logo=flask&logoColor=white">
  <img src="https://img.shields.io/badge/MySQL-8.0-orange.svg?style=for-the-badge&logo=mysql&logoColor=white">
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white">
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white">
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black">
</p>

---

## 🏷️ Logo

<p align="center">
  <img src="static/images/logo.png" alt="Vyra Logo" width="300">
</p>

---

## 🚀 About the Project

**VYRA** is a full-stack Food ordering  Tracking System built using **Python (Flask)** and **MySQL**, designed to simulate real-world platforms like **Swiggy** and **Zomato**.

Whether you're a student learning full-stack development, a beginner exploring Flask, or someone curious about how food ordering systems work — VYRA provides a complete, working example to learn from.

---

## 🎯 Who is This Project For?

| Audience | Why |
|----------|-----|
| 👨‍🎓 **Students** | Learn DBMS + Web Development integration |
| 🧑‍💻 **Beginners** | Explore Flask backend logic |
| 🍔 **Developers** | Understand real-time tracking systems |
| 📚 **Educators** | Use as teaching material |

---

## ✨ Features

### 👤 User Features

| Feature | Description |
|---------|-------------|
| 🍕 **Browse Menu** | View food items with prices and restaurants |
| 🔍 **Search & Filter** | Search by food name, filter by restaurant |
| 🛒 **Add to Cart** | Select quantities and add to cart |
| 💳 **Place Orders** | Direct order or cart checkout |
| 📦 **Live Tracking** | Real-time status updates every 2 seconds |
| 📜 **Order History** | View all past orders by User ID |
| 🔄 **Auto Refresh** | Tracking page updates automatically |

### ⚙️ System Features

| Feature | Description |
|---------|-------------|
| 🔄 **Auto Status Updates** | Background thread updates order status automatically |
| 📊 **Progress Bar** | Visual delivery progress (25% → 100%) |
| ⏱️ **Countdown Timer** | Shows when next status will update |
| 🎯 **Multi-User Support** | 50+ users with independent sessions |
| 🧠 **Smart Cart** | Items persist after page refresh |

---

## 🧱 Built With

### 🎨 Frontend

| Technology | Purpose |
|------------|---------|
| **HTML5** | Page structure |
| **CSS3** | Styling, gradients, animations |
| **JavaScript** | Interactivity, API calls, dynamic updates |

### ⚙️ Backend

| Technology | Purpose |
|------------|---------|
| **Python 3.8+** | Core programming language |
| **Flask** | Web framework for APIs |
| **Flask-CORS** | Cross-origin request handling |
| **Threading** | Background auto-updater |

### 🗄️ Database

| Technology | Purpose |
|------------|---------|
| **MySQL 8.0** | Relational database management |
| **MySQL Connector** | Python-MySQL connection |

---

## 🖼️ Screenshots

### 🏠 Home Page
*Main landing page with navigation to all features*

![Home Page](Screenshots/HOME%20PAGE.png)

---

### 🍽️ Menu Page
*Browse food items with search and restaurant filter*

![Menu Page](Screenshots/Menu.png)

---

### 🛒 Place Order Page
*Add items to cart with quantity controls*

![Place Order Page](Screenshots/Place%20Order.png)

---

### 💼 Cart Page
*Review cart, update quantities, remove items, and checkout*

![Cart Page](Screenshots/Cart.png)

---

### 📦 Track Order Page
*Live order tracking with progress bar and auto-refresh every 2 seconds*

![Track Order Page](Screenshots/Track%20Order.png)

---

## ⏱️ Auto Status Timeline

| Time | Status | Progress |
|------|--------|----------|
| 0 sec | 🟠 **Order Placed** | 25% |
| 5 sec | 🔵 **Preparing** | 50% |
| 20 sec | 🟣 **Out for Delivery** | 75% |
| 50 sec | 🟢 **Delivered** | 100% |

---

## 📂 Database Schema

The application uses **7 interconnected tables**:

```sql
-- Users table
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    email VARCHAR(100),
    password VARCHAR(100)
);

-- Restaurants table
CREATE TABLE restaurants (
    restaurant_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    location VARCHAR(100)
);

-- Menu table
CREATE TABLE menu (
    item_id INT PRIMARY KEY AUTO_INCREMENT,
    restaurant_id INT,
    item_name VARCHAR(100),
    price DECIMAL(10,2),
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id)
);

-- Cart table
CREATE TABLE cart (
    cart_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    item_id INT,
    quantity INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (item_id) REFERENCES menu(item_id)
);

-- Orders table
CREATE TABLE orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    order_time DATETIME,
    total_amount DECIMAL(10,2),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Order Items table
CREATE TABLE order_items (
    order_item_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT,
    item_id INT,
    quantity INT,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (item_id) REFERENCES menu(item_id)
);

-- Order Status table
CREATE TABLE order_status (
    status_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT,
    status VARCHAR(50),
    updated_time DATETIME,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
```
---




## 🔌 API Endpoints

### Page Routes (GET)

| Route | Page |
|-------|------|
| `/` | Home Page |
| `/menu` | Menu Page |
| `/place_order_page` | Order Page |
| `/cart_page` | Cart Page |
| `/track` | Tracking Page |
---

### API Routes

| Route | Method | Purpose |
|-------|--------|---------|
| `/api/menu` | GET | Fetch all menu items |
| `/api/cart/add` | POST | Add item to cart |
| `/api/cart/<user_id>` | GET | Get user's cart |
| `/api/cart/update` | PUT | Update cart quantity |
| `/api/cart/remove/<id>` | DELETE | Remove from cart |
| `/api/cart/checkout` | POST | Convert cart to order |
| `/place_order` | POST | Place direct order |
| `/order_status/<id>` | GET | Get current status |
| `/order_history/<id>` | GET | Get status timeline |
| `/user_orders/<id>` | GET | Get user's all orders |

---

## 🔧 Installation

### Prerequisites

- Python 3.8 or higher
- MySQL Server 8.0

### Step 1: Clone the repository

```bash
git clone https://github.com/chiragroshan18/vyra-food-tracker.git
cd vyra-food-tracker
```
---

### Step 2: Install dependencies
```bash
pip install flask flask-cors mysql-connector-python
```
---

### Step 3: Create database
```bash
mysql -u root -p
CREATE DATABASE vyra_food_tracker;
USE vyra_food_tracker;
```
---

###  Step 4: Update database credentials in app.py
```bash
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="vyra_food_tracker"
)
```
---
### Step 5: Run the application
```bash
python app.py
```
---

### Step 6: Open browser
```bash
http://127.0.0.1:5000
```
---
## 🧭 Usage Guide
```
Step 1: BROWSE MENU
        ↓
    View all food items with prices and restaurants
        ↓
Step 2: ADD TO CART
        ↓
    Select quantities and click "Add to Cart"
        ↓
Step 3: VIEW CART
        ↓
    Review items, update quantities, remove items
        ↓
Step 4: CHECKOUT
        ↓
    Click "Proceed to Checkout" → Order created
        ↓
Step 5: TRACK ORDER
        ↓
    0s:  🟠 Order Placed (25%)
    5s:  🔵 Preparing (50%)
    20s: 🟣 Out for Delivery (75%)
    50s: 🟢 Delivered (100%)
        ↓
Step 6: ORDER HISTORY
        ↓
    View all past orders and track any order
```

---

## Test Users

| User ID | Name      | Email               |
|---------|-----------|---------------------|
| 23      | Sudhher   | sudhher@gmail.com   |
| 24      | Chirag    | chirag@gmail.com    |
| 25      | Nandhini  | nandhini@gmail.com  |


---


## 🏗️ Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              VYRA FOOD TRACKER                              │
│                           PIPELINE ARCHITECTURE                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   app.py        │     │   templates/    │     │   static/       │
│   Main Flask    │────→│   index.html    │────→│   css/          │
│   Application   │     │   menu.html     │     │   style.css     │
│                 │     │   order.html    │     │   images/       │
│                 │     │   cart.html     │     │   logo.png      │
│                 │     │   track.html    │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘

                              │
                              ▼

┌─────────────────────────────────────────────────────────────────────────────┐
│                           API ENDPOINTS                                     │
│  /api/menu  │  /api/cart/add  │  /api/cart/checkout  │  /order_status/<id>  │
└─────────────────────────────────────────────────────────────────────────────┘

                              │
                              ▼

┌───────────────────────────────────────────────────────────────────────────────┐
│                         AUTO STATUS UPDATER                                   │
│                      (Background Thread - Threading)                          │
│                                                                               │
│ Order Placed (0s) → Preparing (5s) → Out for Delivery (20s) → Delivered (50s) │
└───────────────────────────────────────────────────────────────────────────────┘

                              │
                              ▼

┌───────────────────────────────────────────────────────────────────────────────┐
│                           DATABASE (MySQL)                                    │
│                                                                               │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌───────────┐ ┌───────────┐  │  
│  │  users  │ │  menu   │ │ orders  │ │  cart   │ │restaurant │ │orderitems │  │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └───────────┘ └───────────┘  │  
│                                                                               │
│  ┌─────────────┐                                                              │
│  │order_status │                                                              │
│  └─────────────┘                                                              │
└───────────────────────────────────────────────────────────────────────────────┘
```

---

## 🗂️ Project Structure

```bash
vyra-food-tracker/
├── 🐍 app.py — Main Flask application
├── 📁 templates/
│   ├── 🏠 index.html — Home page
│   ├── 🍽️ menu.html — Menu page
│   ├── 🛒 order.html — Order page
│   ├── 💼 cart.html — Cart page
│   └── 📦 track.html — Tracking page
├── 📁 static/
│   ├── 🎨 css/
│   │   └── style.css — Stylesheet
│   └── 🖼️ images/
│       └── logo.png — Logo image
├── 📁 Screenshots/
│   ├── HOME PAGE.png
│   ├── Menu.png
│   ├── Place Order.png
│   ├── Cart.png
│   └── Track Order.png
└── 📄 README.md
```

---

## 💡 Key Features

| Feature                  | Why It's Special                                                   |
|--------------------------|--------------------------------------------------------------------|
| 🔄 Auto Status Updates   | No manual intervention, background thread handles everything       |
| 📦 Live Tracking         | Updates every 2 seconds automatically, no refresh required         |
| 📊 Progress Bar          | Visual representation of delivery progress                         |
| ⏱️ Countdown Timer       | Shows exactly when next status will change                         |
| 🎯 Multi-User Support    | Each user has independent cart and orders                          |
| 🧠 Cart Persistence      | Items saved even after page refresh                                |

---


## 🔐 Security Features

| Feature                     | Description                                      |
|----------------------------|--------------------------------------------------|
| 🔒 Password Hashing        | For secure user authentication                   |
| 🛡️ Input Validation       | Applied on all forms to prevent invalid input    |
| 🧼 SQL Injection Protection| Using parameterized queries                      |
| 🧰 Error Handling          | Proper rollback on failures                      |

---

## 📊 Project Metrics

| Metric                     | Value              |
|---------------------------|--------------------|
| Total Users Supported     | 50+               |
| Database Tables           | 7                 |
| API Endpoints             | 15+               |
| Web Pages                 | 5                 |
| Status Update Times       | 5s, 20s, 50s      |
| Tracking Refresh Rate     | Every 2 seconds   |
| Lines of Code (Backend)   | ~500              |
| Lines of Code (Frontend)  | ~800              |

---

## 🙏 Acknowledgements

Every project is a journey — and **VYRA** was no exception. Here's a heartfelt note of gratitude:

- 🙏 The countless hours of learning Flask and MySQL  
- 💻 Experimenting with real-time tracking systems  
- 🛠️ Debugging struggles that turned into learning moments  
- ✍️ The art of documenting code and explaining concepts  
- ⚙️ Building from scratch — from first line to final polish

  ---

## 👥 Project Team

### Team Name: **🍽️ Vyanjan Yatra**

| Name | Role | GitHub |
|------|------|--------|
|  **Chintapatla Sudheer Naidu** | 🗄️ Database Designer | [@chintapatla-sudheer934](https://github.com/chintapatla-sudheer934) |
| **Chittem Nandhini** | 🗄️ Database Designer | [@chittemnandhini-darsh](https://github.com/chittemnandhini-darsh) |
| **Chirag Roshan** |🖥️ Full-Stack Developer | [@chiragroshan18](https://github.com/chiragroshan18) |

## 📄 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

## 🌐 Connect

- If you're interested in **Python projects, Flask development, or real-time food delivery systems** — feel free to connect with us on LinkedIn or open a discussion here.

- **Chintapatla Sudheer Naidu** – [LinkedIn](https://www.linkedin.com/in/chintapatla-sudheer-naidu-b04353349/)
- **Chittem Nandhini** – [LinkedIn](https://www.linkedin.com/in/nandhini-chittem-21a871400/)
- **Chirag Roshan** – [LinkedIn](https://www.linkedin.com/in/chirag-roshan18/)
  

  ---





