# BRAIN TEASER
This project is the implementation of a RESTful API backend for a Trivia web application using Flask and Flask-CORS. The frontend and data models had already been provided by the Udacity staff team. Our task was to complete several endpoints using Test-Driven Developement methods to implement the intended functionality of the app.

In it's complete state, the web app allows users to view questions and their answers in various categories eg. science, art etc. One can also search for specific questions on the search bar. Once feeling confident, a user can attempt to play the quiz game where they will be asked 5 random questions and shown their final score.

All the code for the API follows PEP8 guidelines.

## Getting Started
### Pre-requisites
The following should be installed: Python3, pip, postgresql node

### Setting up the backend
1) Database:
 - Start the postgres server. For Linux users: `sudo service postgresql-9.3 start`
 - Log onto the psql command line tool. Run `sudo -u postgres psql`
 - Create the trivia database by running `createdb trivia`
 - cd into the backend folder and populate the database using the trivia.psql file provided. `psql trivia < trivia.psql`

2) Dependencies
 - Create a virtual environment and activate it. Run:
 ```
 virtualenv venv 
 source venv/bin/activate
 ```
 - cd into the /backend folder and run `pip install -r requirements.txt` to install all dependencies.
 
3) Flask Server
 - While in the /backend folder, you will need to run the following 2 commands the first time:
 ```
 export FLASK_APP=flaskr
 export FLASK_ENV=development
 ```
 - To start the server, use the command `flask run`
 
 4) Setting up the testing database
 - Run the following commands to set up the test database
 ```
 dropdb trivia_test
 createdb trivia_test
 psql trivia_test < trivia.psql
 ```
 - To run the tests in test_flaskr.py, run `python3 test_flaskr.py`
 
 ### Setting up the frontend
 1) cd into /frontend folder
 2) Run `npm install` to install required packages.
 3) Run `npm start` to run the app
 
 ## The API Reference
 ### Getting started
 The app is hosted locally, hence the base URL for the api is:
 
 `http://127.0.0.1:5000/`
 No Authorization or API Key required.
 
 ### Data Format
 All the data is returned as JSON objects.
 
 ### Errors
 While using the API, you may encounter one of the following errors:
 -Error 400: Bad Request
 -Error 404: Resource Not Found
 -Error 405: Method not allowed
 -Error 422: Not Processable.
 These errors will be sent back in the following format:
 
 ```
 {
    "success": False, 
    "error_code": 404,
    "message": "resource not found"
 }
 ```
 ### Endpoints
 
 *Note:* All endpoints return a status_code and an accompanying success message.
 
 
 1) GET /categories
 Example: `curl http://127.0.0.1:5000/categories`
 
 Required arguements: None
 
 Returns: A categories object whose value is an object containing all the category IDs as keys and the category types as the values. 
 
 Expected response:
 ```
 {
   "categories": {
      "1": "Science",
      "2": "Art",
      "3": "Geography",
      "4": "History",
      "5": "Entertainment",
      "6": "Sports"
     },
    "status_code": 200,
    "success": true
 }
 ```
 
 2) GET /questions
 Example: `curl http://127.0.0.1:5000/questions?page=1`
 
 Required arguements: page number (?page=1)
 
 Returns: An objects with the following key:value pairs:
     questions: A list of 10 questions available on every page
     total_questions: The total number of questions available on the database
     current_category: Usually returns the id of the 1st category
     categories: An object containing all the category IDs as keys and the category types as the values.
 
 Expected response:
 ```
 "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": 1, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ], 
  "status_code": 200, 
  "success": true, 
  "total_questions": 10
 ```
 3) DELETE /questions/{question_id}
 Example: `curl -X DELETE http://127.0.0.1:5000/questions/1`
 
 Required arguements: None
 
 Returns: Status code and success message.
 
 Expected response:
 ```
 {
 "status_code": 200, 
 "success": true, 
 }
 ```
 4) POST /questions
 Example: `curl -X POST -d '{"question":"What colour is produced from adding red and blue","answer": "purple","difficulty": 2,"category": 1}' http://127.0.0.1:5000/questions`
 
 Required arguements: None
 
 Returns: Status code and success message.
 
 Expected response:
 ```
 {
 "status_code": 200, 
 "success": true, 
 }
 ```
 
 5) POST /questions/search
 Example: `curl -X POST -d '{"searchTerm":"actor"}' http://127.0.0.1:5000/questions/search`
 
 Required arguements: None
 
 Returns: An object with the following key:value pairs:
     questions: A list of questions containing the search term
     total_questions: Total number of questions returned
     current_category: Usually returns the id of the first category
 
 Expected response:
 ```
 {
     "questions":{
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
     },
     "total_questions": 1,
     "currentCategory": 1,
     "status_code": 200, 
     "success": true
 }
 ```
 6) GET /categories/{category_id}/questions
 Example: `curl http://127.0.0.1:5000/categories/2/questions`
 
 Required arguements: None
 
 Returns: An object with the following key:value pairs:
     questions: A list of questions contained in that category
     total_questions: Total number of questions returned
     current_category: The id of the requested category
     
 Expected response:
 ```
 {
  "current_category": 2, 
  "questions": [
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ], 
  "status_code": 200, 
  "success": true, 
  "total_questions": 4
}
 ```
 7) POST /quizzes
 Example: `curl -X POST -d '{"quiz_category":"{"History": 4}","previous_questions":[]}' http://127.0.0.1:5000/quizzes`
 
 Required arguements: None
 
 Returns: An object with a key of 'question' whose value is an array with a random question to be asked in the quiz
 
 Example response:
 ```
 {
     "question": {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
     }
 }
 ```
 
 ## Deployment
 The app has not been deployed and is hosted locally.
 
 ## Authors
  Richard Gichuki. [Find me here](https://github.com/ChadGichuki)
  Udacity Staff team.
  
 ## Acknowledgements
  My ALX-T Fullstack Nanodegree Session Lead BUSUYI OWOYEMI for the weekly connect sessions.
  Coach Caryn from Udacity for the amazing lessons on RESTful API development.