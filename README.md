# Nimbus Weather

A full-stack weather application built with Python, Flask, JavaScript, HTML, and CSS.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Deployment](https://img.shields.io/badge/Render-Live-success)

## Live Demo

Application:

https://nimbus-705w.onrender.com/

Repository:

https://github.com/yakshamaan/Nimbus-Weather



## Overview

Nimbus Weather is a web application that provides real-time weather information for locations around the world. Users can search for any city, view current weather conditions, and retrieve weather data based on their current location using the browser's geolocation capabilities.

This project began as a simple Python weather application and gradually evolved into a complete web application with a responsive frontend, API integration, and cloud deployment. The goal was to gain hands-on experience with full-stack development while building something practical and useful.



## Features

- Search weather information for any city worldwide
- Detect and display weather based on the user's current location
- Real-time temperature updates
- Weather condition descriptions and icons
- Air Quality Index (AQI) monitoring
- Sunrise and sunset information
- Humidity monitoring
- Wind speed information
- Atmospheric pressure data
- Visibility measurements
- Interactive weather map
- Responsive design for desktop and mobile devices
- Clean and user-friendly interface



## Screenshots

### Homepage

<img width="1450" height="860" alt="image" src="https://github.com/user-attachments/assets/38cf3d91-cd6a-4d0a-b64d-e55aa90f83f3" />


### Weather Search Results

<img width="1450" height="860" alt="image" src="https://github.com/user-attachments/assets/3d1ea610-b9fa-49dc-8ccc-d57af5765a77" />

### Air Quality Index

<img width="1450" height="1560" alt="image" src="https://github.com/user-attachments/assets/e85986e0-f168-4750-8045-185fd6df263f" />


### Mobile View

<p align="center">
  <img src="https://github.com/user-attachments/assets/ffd6b656-38ca-4c83-bd14-093c8d914869" height="500">
  <img src="https://github.com/user-attachments/assets/07bd7c63-70ff-40a1-8c82-39e6a2fea358" height="500">
</p>



## Tech Stack

### Backend

* Python
* Flask

### Frontend

* HTML5
* CSS3
* JavaScript

### APIs

* OpenWeatherMap API for real-time weather data
* Browser Geolocation API

### Deployment

* Render



## How It Works

1. A user enters a city name or allows location access.
2. The frontend sends a request to the Flask backend.
3. Flask communicates with the weather API.
4. The API returns current weather information.
5. The backend processes and formats the data.
6. The frontend displays the weather details to the user.



## Development Journey

Rather than building the final application all at once, I developed Nimbus Weather incrementally, adding new features and improving the user experience with each iteration.

### Phase 1: Basic Weather Application

The project started as a simple Python application that fetched and displayed current weather information for a user-entered city using a weather API. The focus was understanding API requests, handling JSON responses, and presenting weather data.

### Phase 2: Flask Integration

After building the basic version, I migrated the project to Flask to create a full web application. This allowed me to connect a Python backend with a frontend built using HTML, CSS, and JavaScript.

### Phase 3: 5-Day Weather Forecast

I expanded the application to display forecast data instead of only current conditions. This required processing larger API responses and organizing forecast information in a user-friendly format.

### Phase 4: Animated Weather Icons

To improve the visual experience, I added animated weather icons that dynamically change based on current weather conditions. This made the interface more engaging and informative.

### Phase 5: Location Detection

Using the Browser Geolocation API, I implemented automatic location detection. Users can now retrieve weather information for their current location without manually searching for a city.

### Phase 6: Sunrise and Sunset Information

Additional weather details such as sunrise and sunset timings were integrated to provide a more complete overview of daily weather conditions.

### Phase 7: Air Quality Index (AQI)

The application was extended to include air quality information, allowing users to monitor environmental conditions alongside traditional weather data.

### Phase 8: Interactive Weather Map

An interactive weather map was added to help users visualize weather patterns and explore conditions across different regions.

### Phase 9: Glassmorphism UI Redesign

The final major improvement focused on user experience and design. The interface was redesigned using modern glassmorphism-inspired components, improving aesthetics while maintaining usability across desktop and mobile devices.



## Installation and Setup

### Clone the Repository

```bash
git clone https://github.com/your-username/nimbus-weather.git
cd nimbus-weather
```

### Create a Virtual Environment

```bash
python -m venv venv
```

### Activate the Environment

Windows:

```bash
venv\Scripts\activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file in the project root:

```env
OPENWEATHER_API_KEY=your_api_key_here
```

### Run the Development Server

```bash
python main.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000
```



## Project Structure

```text
Nimbus-Weather/
│
├── .vscode/
│   └── settings.json
│
│
├── static/
│   ├── bg/
│   ├── lottie/
│   └── style.css
│
├── templates/
│   └── index.html
│
├── weather_app/
│
├── .gitignore
├── main.py
├── package.json
├── package-lock.json
├── render.yaml
├── requirements.txt
└── README.md
```



## Challenges Faced

One of the biggest challenges was connecting the frontend and backend while keeping the user experience smooth and responsive. Working with external APIs introduced several edge cases, including invalid city names, missing weather data, and network-related issues.

Another challenge was deploying the application to Render and configuring environment variables securely without exposing API keys. Implementing browser geolocation also required handling permissions and fallback scenarios when location access was denied.



## What I Learned

Through this project, I gained experience with:

* Building backend applications using Flask
* Designing responsive user interfaces
* Consuming and processing third-party API data
* Connecting frontend and backend components
* Working with asynchronous JavaScript requests
* Handling user location data through browser APIs
* Deploying web applications to the cloud
* Using Git and GitHub for version control
* Managing environment variables securely

This project was an important step in moving from standalone Python scripts to complete full-stack web applications.


## Key Takeaways

This project taught me that building software is rarely a one-step process. Starting from a simple command-line script and gradually evolving it into a deployed full-stack application helped me understand debugging, iteration, deployment, and designing for real users.

## Future Improvements

Planned features and enhancements include:

* 7-day weather forecasts
* Hourly weather predictions
* Search history
* Favorite and saved locations
* Weather notifications
* PWA support
* Historical weather trends
* Unit conversion (°C/°F)
* Severe weather alerts
* Dark mode support
* Improved visualizations and charts
* Weather comparison between multiple cities
