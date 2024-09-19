# Food Facilities Challenge

# Description
This project provides a backend API and a basic user interface for a mobile food facilities finder application.
Users can search for food facilities by applicant name, street location (partial address search), or by their
current location (using longitude and latitude).

# Solution
The application utilizes:
* **Backend:** The backend provides API endpoints to handle the search queries to return the relevant results in JSON format

* **Frontend:** HTML, CSS and Typescript/Javascript for the user innterface. Material UI is also used for styling
                components and interactivity. It has following features:
    * Search Forms: Three search forms to search by applicant name, partial street address and geographic location.
    * Results Display:  Displays search results.
    * Clear Functionality: Clears displayed results and inpuut fields.

# Technical / Architectural Decisions
1. **Frontend Framework**
    * Material UI - Utilized MUI to provide a consistent look with minimal custom CSS. The responsive components ensure a seamless experience. Pre-built components facilitatedfaster development process and unified design.

2. **Typescript**
    * Asynchronous Functions: Used `async/await` for making requests to ensure a responsive user innterface. This approach simplifies async code, enhances readability and manages errors effectively with try/catch block.

# Critique
**What would you have done differently?**
* *Backend improvements:*
    * Consider using a scalable framework (e.g. Django) since Flask is better suited for prototypes.
    * Implement caching to improve performance.
    * Enhance error handling to return more information regarding errors.
    * Use dedicated database for storing food facilities data.

* *Frontend improvements:*
    * Develop a more visually appealing and responsive UI instead of a basic search form.
    * Implement advanced search filters based on additional dataset attributes.
    * Integrate a map service to visualize food facilities' locations.

**What are the trade-offs you might have made?**
* *Complexity vs Time* - Implementing a basic UI is suitable for a functional prototype, but a polished user experience requires additional features.
* *Simplicity vs. Scalability*: Choosing Flask prioritizes ease of development over scalability features typically required for highly scalable applications.
* *Performance vs. Cost* - Enhancing performance through scalable backends, dedicated databases, or caching would incur additional infrastructure costs.

**What are the things you left out?**
* *Real-time updates* - The application depends on static data. Integrating with services that have real-time data would enhance the user experience.
* *Advcance search filters* - Implement filters based on other data points.
* *Map integration* - Adding a map to the UI would allow users to visualize the locations of food facilities.

**What are the problems with your implementation and how would you solve them if we had to scale the application to a large number of users?**
* *Problems*
    * Scalibility - Flask may become a bottleneck as the number of users increases.
    * Pagination -  There is no server-side pagination.
    * Performance - Relying on an external API for each search may affect performance.
    * Data storage - As data grows, use of a dedicated database would be more efficient.
* *Scaling solutions*
    * Using a scalable framework for building a web application.
    * Implement caching for API responses and frequently accessed data.
    * Optimize queries to avoid unnecessary data retrieval.
    * Distribute the application across multiple servers to enhance scalability and fault tolerance.
    * Continuously monitor application performance and manage increasing loads.
    * Implement lazy loading or infinite scrolling on the UI to handle large data sets.


# Steps to run the application
1. **Setup a virtual environment**
    ```
    python -m venv venv
    source venv/bin/activate 
    ```
2. **Install dependencies**
    ```
    pip install -r requirements.txt
    ```
3. **Run the app**
    ```
    flask run   # or python app.py
    ```
4. View the App (UI): Navigate to `localhost:5000` 

###
* **Automated tests** 
    * To run - ```pytest```
    * If encountering `ModuleNotFoundError`, adjust `PYTHONPATH` before running the tests:
        ```
        export PYTHONPATH=.
        pytest
        ```
           

* **API Documentation** : Access Swagger UI at `localhost:5000/swagger/`