# WasteFood - Food Donation Platform

![WasteFood Hero Image](https://placehold.co/1200x600/42b983/FFFFFF?text=WasteFood&font=lato)

A full-stack web application designed to reduce food waste and fight hunger by connecting food donors with those in need. Built with a modern tech stack featuring Vue.js, Flask, and Supabase.

---

## 🌟 Features

- **User Authentication:** Secure user registration and login handled by Supabase Auth.
- **Food Donation Listings:** Authenticated users can share details about surplus food, including the type, quantity, and pickup location.
- **Interactive Dashboard:** A central hub for users to either list a new donation or view all currently available food items.
- **Request System:** Users can request an available food item, which notifies the donor.
- **Donation Management:** Donors have a dedicated "My Donations" page to track the status of their items and view incoming requests.
- **Approval System:** Donors can approve requests, which updates the status of the food item to "Claimed".
- **Responsive Design:** A mobile-first, professional user interface that works seamlessly on both desktop and mobile devices.

---

## 🛠️ Tech Stack

This project is built with a modern, decoupled architecture.

- **Frontend:** **Vue.js** (v3) with Vue Router for navigation.
- **Backend:** **Flask** (Python) providing a RESTful API.
- **Database:** **Supabase** (PostgreSQL) for data storage.
- **Authentication:** **Supabase Auth** for user management and JWT-based security.
- **Styling:** CSS with responsive media queries.

---

## 🚀 Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

- [Node.js](https://nodejs.org/) (v16 or higher)
- [Python](https://www.python.org/) (v3.10 or higher) and `pip`
- A free [Supabase](https://supabase.com/) account

### Installation & Setup

1.  **Clone the Repository**
    ```sh
    git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
    cd your-repo-name
    ```

2.  **Setup Supabase**
    - Create a new project on your Supabase dashboard.
    - Go to the **SQL Editor** and run the queries found in `database_setup.sql` to create the necessary tables (`profiles`, `food_items`, `requests`) and triggers.
    - Go to **Project Settings -> API** to get your keys.

3.  **Configure Backend**
    - Navigate to the `backend` directory.
    - Create a `.env` file and add your Supabase credentials:
      ```env
      SUPABASE_URL="YOUR_SUPABASE_PROJECT_URL"
      SUPABASE_JWT_SECRET="YOUR_SUPABASE_JWT_SECRET"
      SUPABASE_SERVICE_ROLE_KEY="YOUR_SUPABASE_SERVICE_ROLE_KEY"
      ```
    - Create a virtual environment and install dependencies:
      ```sh
      python -m venv venv
      .\venv\Scripts\activate
      pip install -r requirements.txt
      ```

4.  **Configure Frontend**
    - Navigate to the `frontend` directory.
    - Create a `.env.local` file and add your public Supabase keys:
      ```env
      VITE_SUPABASE_URL="YOUR_SUPABASE_PROJECT_URL"
      VITE_SUPABASE_ANON_KEY="YOUR_SUPABASE_ANON_KEY"
      ```
    - Install the required packages:
      ```sh
      npm install
      ```

### Running the Application

You will need to run the backend and frontend servers in two separate terminals.

1.  **Run the Backend Server** (from the `/backend` directory)
    ```sh
    # Make sure your virtual environment is active
    python app.py
    ```
    The backend will be running at `http://localhost:5000`.

2.  **Run the Frontend Server** (from the `/frontend` directory)
    ```sh
    npm run dev
    ```
    The frontend will be accessible at `http://localhost:5173`.

---

## 📜 License

This project is licensed under the MIT License - see the `LICENSE.md` file for details.
