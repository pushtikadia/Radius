# Radius 📡

This project documents the development of **Radius**, a hyper-local, decentralized disaster relief platform. It focuses on connecting people in immediate proximity during crises by enabling real-time resource sharing and SOS broadcasting without relying on complex external infrastructure.

## 📂 Repository Structure

The code is organized into core backend and frontend components, each handling a specific aspect of the application:

### 1. Backend & Logic (`main.py`)
* **FastAPI Server:** Acts as the central traffic controller, handling API requests for creating posts and fetching nearby data.
* **Geospatial Logic:** Implements the **Haversine Formula** manually to calculate precise distances between users and resources on a spherical surface.
* **Static File Serving:** Automatically serves the frontend files, enabling a unified deployment structure.
* **Database Management:** Handles connections to the SQLite database to store and retrieve live alerts.

### 2. Database Setup (`setup_db.py`)
* **Automatic Initialization:** A standalone script that initializes the `lifeline.db` SQLite database.
* **Schema Design:** Creates the `posts` table with fields for geolocation (`lat`, `lon`), item type (`REQUEST`/`OFFER`), and descriptions.
* **Seeding:** Includes logic to insert dummy data for immediate testing upon setup.

### 3. Frontend Interface (`static/`)
* **Command Center (`index.html`):** A desktop-first dashboard for NGOs and responders. It integrates **Leaflet.js** to visualize all active requests on an interactive map.
* **Field Unit (`mobile.html`):** A lightweight, mobile-first interface designed for victims or volunteers to quickly broadcast their location and needs.
* **Client Logic (`app.js`):** Manages the browser's `navigator.geolocation` API to capture precise coordinates and performs asynchronous `fetch` calls to the backend.
* **Responsive Styling (`styles.css`):** Uses modern CSS to ensure the app works on both large dashboard screens and small mobile devices, with color-coded badges for "Requests" (Red) and "Offers" (Green).

## 🚀 Getting Started

### Prerequisites
To run this project, you need **Python** installed on your machine. The system relies on the following lightweight libraries:
* `fastapi`
* `uvicorn`
* `pydantic`

### How to Run
You can run the platform locally by following these steps:

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Initialize the Database:**
    ```bash
    python setup_db.py
    ```
3.  **Start the Server:**
    ```bash
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ```
4.  **Access the Platform:**
    * **Dashboard:** Open `http://localhost:8000` in your browser.
    * **Mobile:** Connect your phone to the same Wi-Fi and visit `http://<YOUR_LAPTOP_IP>:8000/static/mobile.html`.

## 🛠 Tools Used

* **Python (FastAPI):** High-performance backend logic.
* **SQLite:** Zero-configuration, serverless database engine.
* **Leaflet.js:** Interactive maps for the command center.
* **HTML5/CSS3:** Semantic markup and responsive design.
* **JavaScript (ES6):** Async/Await logic and DOM manipulation.

---
<p align="center">
  <b> Radius </b> • Created by <a href="https://github.com/pushtikadia"><b>Pushti Kadia</b></a>
</p>

