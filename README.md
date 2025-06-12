# EquityGauge
**EquityGauge**: My project to master advanced Python (FastAPI), web development, and CI/CD. It's a financial web app that scrapes and visualizes company P/E ratios. Demonstrates skills in data handling, API design, Pytest, Docker, and GitHub Actions for clean, tested, and deployable code.

## Table of Contents
- [About](#about)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
- [Architecture](#architecture)
- [Testing](#testing)
- [CI/CD](#cicd)
- [Deployment](#deployment)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

---

## About

This project aims to solve the problem of quickly accessing and comparing key financial metrics of various companies. It serves as a personal learning journey and a portfolio piece to showcase proficiency in modern software development practices. The initial version focuses on retrieving and displaying P/E ratios from public financial data sources.

**My Goals for this Project:**
* To deepen my expertise in advanced Python development, especially with FastAPI.
* To apply best practices in web scraping and API development.
* To build a functional and user-friendly web interface for data visualization.
* To implement comprehensive unit and integration testing using Pytest.
* To establish robust CI/CD pipelines with GitHub Actions.
* To gain hands-on experience with Docker and basic cloud deployment (e.g., AWS).

---

## Features

**MVP (Minimum Viable Product) / Current Features:**
- **Company Data Retrieval:** Scrapes P/E ratios for a predefined list of companies from Yahoo Finance.
- **RESTful API:** Provides a simple API to expose scraped company data.
- **Basic Web Visualization:** A straightforward HTML/CSS/JavaScript interface displaying company names, P/E ratios, and a simple rating system.
- **Manual Company Input:** Companies are currently configured through a backend file.
- **Automated Testing Setup:** Initial setup for unit and integration tests using Pytest.
- **Containerization:** Docker support for easy environment setup.

---

## Technologies Used

* **Backend:**
    * [Python](https://www.python.org/)
    * [FastAPI](https://fastapi.tiangolo.com/)
    * [Requests](https://docs.python-requests.org/en/master/)
    * [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) (for web scraping)
    * [Pytest](https://docs.pytest.org/en/stable/) (for testing)
* **Frontend:**
    * HTML, CSS, JavaScript (Vanilla JS for MVP)
* **Deployment & CI/CD:**
    * [Docker](https://www.docker.com/)
    * [GitHub Actions](https://docs.github.com/en/actions)

---

## Getting Started

Follow these steps to get a local copy of the project up and running.

### Prerequisites

* Python 3.9+
* Docker (recommended for development and deployment)
* Git

### Installation

1.  Clone the repository:
    ```bash
    git clone [https://github.com/YOUR_USERNAME/EquityGauge.git](https://github.com/YOUR_USERNAME/EquityGauge.git)
    cd EquityGauge
    ```
2.  **Backend Setup:**
    ```bash
    cd backend
    python -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

### Running the Application

1.  **Run Backend (using Uvicorn):**
    ```bash
    cd backend
    uvicorn main:app --reload
    ```
    The API will be available at `http://127.0.0.1:8000`. Access `http://127.0.0.1:8000/docs` for API documentation (FastAPI Swagger UI).

2.  **Run Frontend:**
    Open the `frontend/index.html` file in your web browser. (For MVP, a simple static file is sufficient).

---

## Architecture

*(Placeholder for now. You will add a description and/or diagram here later.)*

The application follows a client-server architecture:
-   **Backend:** A FastAPI application handles data scraping, business logic, and exposes a RESTful API.
-   **Frontend:** A web interface (HTML/CSS/JS) consumes data from the backend API and displays it.
-   **Data Source:** External financial websites (e.g., Yahoo Finance) are scraped for real-time data.

---

## Testing

Tests are written using `pytest`. To run tests:

```bash
cd backend
pytest
```

---

## CI/CD

This project utilizes **GitHub Actions** for Continuous Integration. The workflow is set up to automatically run tests on every push to the `main` branch, ensuring code quality and stability.

*(Once implemented, you can link directly to your workflow file here, e.g.: [`.github/workflows/main.yml`](.github/workflows/main.yml))*

---

## Deployment

The application is designed for containerized deployment using **Docker**.

Initial deployment will focus on a simple cloud platform like Heroku or Render for quick public access. In future iterations, the goal is to leverage **AWS** services such as EC2 for hosting, providing a more robust and scalable infrastructure.

---

## Future Enhancements

We have exciting plans for **EquityGauge**! Here are some of the key features and improvements targeted for future development:

* **User Interface:** Implement a more dynamic and modern frontend using frameworks like **Vue.js** or **React**, potentially incorporating **Tailwind CSS** for efficient styling.
* **Database Integration:** Transition from file-based storage to a persistent database (e.g., **PostgreSQL**) for robust historical data tracking and improved data management.
* **Advanced Metrics:** Expand the range of financial ratios beyond P/E, including Debt-to-Equity, EPS, Dividend Yield, and more, for deeper company analysis.
* **Historical Data:** Develop functionality to track and visualize historical financial data over time, allowing for trend analysis.
* **User Accounts & Custom Watchlists:** Implement user registration, authentication, and the ability for authenticated users to create and manage their personalized company watchlists.
* **Advanced Analysis/AI Integration:** Explore incorporating more sophisticated analysis techniques or integrating with Large Language Models (LLMs) for AI-driven insights and summaries based on financial data.
* **Robust Error Handling & Logging:** Enhance the application with comprehensive error handling and logging mechanisms to improve reliability and debuggability in production environments.
* **Scalable Cloud Deployment:** Fully deploy the application on **AWS**, leveraging services like EC2, RDS (for managed databases), Lambda (for serverless functions), S3 (for static assets), and potentially ECS/EKS for highly scalable container orchestration.

---

## Contributing

Feel free to open issues or submit pull requests if you have suggestions, spot a bug, or would like to contribute to the project. Your input is highly valued!

---

## License

This project is licensed under the **MIT License**. You can find the full license details in the [LICENSE](LICENSE) file.
