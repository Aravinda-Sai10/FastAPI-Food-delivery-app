# 🍔 QuickBite Food Delivery API (FastAPI Backend Project)

## 📖 Project Description

QuickBite Food Delivery API is a backend REST API system developed using **FastAPI**.  
This project simulates a real-world food ordering platform where users can browse menu items, filter products, place orders, manage cart operations, and perform advanced search and pagination operations.

This project was developed as part of my **FastAPI Internship training at Innomatics Research Labs**.

---

## 🚀 Key Features

### Menu Management
• View all menu items  
• Get menu item by ID  
• Menu summary statistics  
• Filter menu by category, price, availability  
• Search menu by name and category  
• Sort menu items  
• Pagination support  
• Combined browse endpoint  

### Order Management
• Place orders  
• Order validation  
• Delivery vs pickup calculation  
• Order history tracking  
• Search orders by customer  
• Sort orders by total price  

### Cart Workflow
• Add items to cart  
• Update cart quantity  
• Remove cart items  
• Checkout workflow  
• Automatic order creation  
• Cart clearing after checkout  

### Backend Features
• REST API development
• Pydantic validation
• Helper functions
• Error handling
• Swagger API testing

---

## 🛠 Tech Stack

**Backend:**
• Python
• FastAPI
• Pydantic
• Uvicorn

**Tools:**
• Swagger UI
• VS Code
• GitHub

---

## 📂 Project Structure
QuickBite_Project

│── main.py
│── requirements.txt
│── README.md
│── screenshots

---

## ⚙ Installation Guide

### Step 1 — Clone repository


git clone https://github.com/YOUR_GITHUB_LINK


### Step 2 — Open project folder


cd project_folder


### Step 3 — Create virtual environment


python -m venv venv


### Step 4 — Activate environment

Windows:


venv\Scripts\activate


### Step 5 — Install dependencies


pip install -r requirements.txt


### Step 6 — Run FastAPI server


uvicorn main:app --reload


### Step 7 — Open Swagger UI


http://127.0.0.1:8000/docs


---

## 📸 Project Screenshots

### Menu API
<img src="screenshots/Q2_get_all_items.png" width="500">


### Order Creation
<img src="screenshots/Q8_place_order.png" width="500">
### Cart Checkout
<img src="screenshots/Q15_checkout.png" width="500">
### Menu Filtering
## Pagination
<img src="screenshots/Q18_pagination.png" width="500">
### Pagination
<img src="screenshots/Q18_pagination.png" width="500">
---

## 📌 Important API Endpoints

### Menu APIs

GET /menu
• GET /menu/{item_id}
• GET /menu/filter
• GET /menu/search
• GET /menu/sort
• GET /menu/page
• GET /menu/browse


### Order APIs

• POST /orders
• GET /orders
• GET /orders/search
• GET /orders/sort


### Cart APIs


• POST /cart/add
• GET /cart
• DELETE /cart/{item_id}
• POST /cart/checkout


---

## 🎯 Learning Outcomes

Through this project I learned:

• FastAPI backend development  
• REST API design  
• Data validation using Pydantic  
• Query parameters handling  
• CRUD operations  
• API workflow design  
• Pagination techniques  
• Real-world backend architecture  

---

## 🔮 Future Improvements

• Database integration (MongoDB/PostgreSQL)  
• User authentication  
• Payment gateway integration  
• Order tracking  
• Admin dashboard  

---

## 👨‍💻 Author

**Aravinda Sai**

B.Tech AIML Student  
Aspiring AI Engineer 

---

## 🙏 Acknowledgement

This project was completed as part of my internship training at:

**Innomatics Research Labs**

---

## ⭐ Support

If you like this project:

Give it a ⭐ on GitHub.

## 📌 Project Type
Internship Project

## 🏫 Organization
Innomatics Research Labs

## 📅 Duration
FastAPI Internship Program
