# 💰 Finance Tracking App (Django)

## 🌟 Project Overview

This project is a **Finance Tracking App** built using Django that enables users to track and visualize their financial transactions. By integrating third-party APIs like **Plaid**, dynamic front-end technologies, and robust back-end functionalities, the app delivers an interactive and feature-rich experience for end-users. Here’s a detailed breakdown of the features:

---

## 🚀 **Features Overview**

### 🔗 **1. Plaid API Integration**

- **Purpose**: Fetch and manage users' financial transactions securely.
- **Sandbox Environment**:
  - A custom sandbox user (`custom_nuraly`) was created for testing purposes, simulating real-world use cases.
  - All interactions, such as token creation, exchange, and fetching transactions, are handled via Plaid’s sandbox environment.
- **Transaction Fetching**:
  - Transactions are retrieved using Plaid’s API for a user-selected date range.
  - Multiple retries are implemented to handle potential API delays (`PRODUCT_NOT_READY` error).
  - Transactions are serialized and stored dynamically for use in visualizations and reporting.
- **🔒 Secure Management**:
  - API keys and environment variables (like `PLAID_CLIENT_ID` and `PLAID_SECRET`) are stored securely using `.env` files.
  - Django’s settings utilize `python-decouple` for environment variable management, ensuring no sensitive information is exposed.

---

### 📊 **2. Interactive Dashboard**

The app features an **interactive dashboard** where users can view, analyze, and filter their transactions in real-time.

#### **Key Components**

- **💼 Dynamic Transaction Table**:
  - Displays transactions with columns for **Date**, **Name**, **Category**, and **Amount**.
  - Filters:
    - Users can filter transactions by selecting a specific month.
    - Real-time updates occur when a new month is selected.

- **📈 Data Visualizations**:
  - Built using **Plotly.js** for seamless and interactive charts:
    1. **Bar Chart**:
       - Displays the top 10 transactions for the selected month, sorted by amount.
    2. **Pie Chart**:
       - Highlights the top 5 highest expenses in the selected month.
    3. **Income vs. Expenses**:
       - A side-by-side bar chart for visualizing income (refunds) versus expenses.

- **🔮 Dynamic Projection**:
  - Integrates a **Linear Regression model** to predict future expenditures:
    - Users can dynamically update the projection based on the selected month.
    - Historical data is combined with predictions and displayed as a line chart.

#### **📱 Responsive Design**

- Optimized the dashboard for multiple devices (desktop, tablet, mobile) using a combination of CSS and Django template styling.

---

### 🗺️ **3. Dynamic Entity-Relationship Diagram (ERD) Creation**

To map and visualize the database schema effectively, the following tools and commands were used:

- **🛠️ Tools**:
  - `django-extensions`: A Django package used to generate model diagrams.
  - `graphviz`: An external visualization tool for rendering ERDs.

- **📋 Steps**:
  1. Installed necessary dependencies:

     ```bash
     pip install django-extensions graphviz
     ```

  2. Used the following command to generate the `.dot` file for the database schema:

     ```bash
     ./manage.py graph_models -a > my_project.dot
     ```

  3. Converted the `.dot` file to a visual `.png` representation:

     ```bash
     dot -Tpng my_project.dot -o my_project_ERD.png
     ```

  4. Result:
     - **`.dot` File**: Useful for further customizations and updates to the schema.
     - **`.png` File**: A quick and clear visualization of the database relationships, including models like `User`, `Profile`, `Transaction`, and others.

---

### 🔐 **4. User Authentication and Profile Management**

- **User Signup and Login**:
  - Leveraged Django’s built-in authentication system to manage user accounts securely.
  - Implemented custom views to support user registration and authentication.

- **👤 User Profiles**:
  - Each user has a profile linked to their account, including a `Plaid Access Token`.
  - Profiles are dynamically updated with fetched transaction data.

- **🗑️ Account Deletion**:
  - Users can delete their accounts by providing a confirmation step (re-entering their username).

---

### 🔧 **5. Backend Logic and API Design**

#### **📂 Data Fetching and Management**

- **Fetching Transactions**:
  - Transactions are retrieved via the **Plaid Transactions API**.
  - Handles API errors gracefully (e.g., `PRODUCT_NOT_READY`) by retrying the request.

- **API Endpoints**:
  - A REST API was implemented using **Django Rest Framework** (DRF):
    - `GET /transactions/`: Retrieves all transactions for the authenticated user.
    - `GET /profile/`: Fetches user profile details.
    - `GET /api/expenditure-projection/`: Returns historical and predicted expenditure data.

#### **🔢 Linear Regression for Projections**

- **Scikit-learn**:
  - Used `LinearRegression` from Scikit-learn to build a simple model.
  - Predicts future expenditures based on historical data.
- **Integration**:
  - Predictions are served dynamically to the frontend via an API endpoint.

---

### 🌍 **6. Secure Deployment**

- **Environment Setup**:
  - All sensitive keys and environment variables are stored in `.env` files.

- **🚨 Error Handling**:
  - Detailed logging for debugging and monitoring:
    - `logger.warning()` for recoverable errors like retrying Plaid API requests.
    - `logger.error()` for critical issues such as API exceptions.
  - Graceful error messages displayed to users for better UX.

---

## ⭐ **What Makes This Project Unique?**

1. **🔗 End-to-End Integration**:
   - Combines robust API integration, backend logic, and frontend interactivity seamlessly.

2. **📊 Real-Time Data Insights**:
   - Users get instant insights into their financial habits through dynamic visualizations.

3. **⚙️ Customizability**:
   - Features like dynamic filtering, prediction models, and ERD creation ensure the app is flexible and extensible.

4. **📈 Scalability**:
   - Designed to support multiple users with personalized dashboards and secure profile management.

5. **📚 Educational Use Case**:
   - Demonstrates the integration of third-party APIs (Plaid), machine learning (Linear Regression), and dynamic data visualization in a practical project.

---

## 📜 License

This project is licensed under the [MIT License](./LICENSE).

## 📅 **Next Steps**

- 🔄 Expand projection capabilities to use more advanced machine learning models.
- 💵 Add user budgeting features with alerts for overspending.
- 📊 Enhance the UI with additional visualizations like monthly trends or category breakdowns.

---

This project serves as a comprehensive demonstration of integrating third-party APIs, creating interactive dashboards, and building a data-driven financial application with Django. Let me know if you'd like further details on any specific aspect!
