import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from settings import DB_NAME, DB_USER, DB_PASSWORD


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path ="postgres://{}:{}@{}/{}".format('student', 'student','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            
        # New question to test post requests
        self.new_question = {
            "question": "What colour is produced from adding red and blue",
            "answer": "purple",
            "difficulty": 2,
            "category": 1
        }
        
        # Testing play quiz by specific category
        self.quiz = {
            "quiz_category":1,
            "previous_questions": [] 
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    
    def test_get_all_categories(self):
        """
        Tests if we are able to retrieve an array of all the categories available on our database
        """
        response = self.client().get('/categories')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])
        self.assertEqual(len(data["categories"]), 6)
    
    def test_get_all_questions_paginated(self):
        """
        Tests if we are able to retrieve the questions available on the database. 
        The questions should be paginated in 10 questions per page
        """
        response = self.client().get('/questions?page=1')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(len(data["questions"]), 10)
        self.assertTrue(data["current_category"])
        self.assertTrue(data["categories"])
        self.assertTrue(data["total_questions"])
        
    def test_404_for_request_to_non_existent_questions_page(self):
        """
        Tests if an error 404 is thrown if a request if made for a page beyond the pages
        available on the database
        """
        response = self.client().get('/questions?page=11')
        data = json.loads(response.data)
        
        self.assertEqual(data["error_code"], 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
        
    def test_delete_quetion(self):
        """
        Tests if a question of a given id is deleted from the database.
        """
        response = self.client().delete('/questions/19')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        
    def test_422_for_deleting_non_exist_question(self):
        """
        Tests if an error 422 is raised when trying to delete a question with an ID
        that doesn't exist.
        """
        response = self.client().delete('questions/1500')
        data = json.loads(response.data)
        
        self.assertEqual(data["error_code"], 422)
        self.assertEqual(data["message"], "unprocessable")
        self.assertEqual(data["success"], False)
        
    def test_post_a_new_question(self):
        """
        Tests if a new question is added to the database using a post request
        """
        response = self.client().post('/questions', json=self.new_question)
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        
    def test_405_for_posting_new_question_to_wrong_path(self):
        """
        Tests if error 405 (method not allowed) is thrown when trying to post
        a question to the wrong path
        """
        response = self.client().post('/questions/1', json=self.new_question)
        data = json.loads(response.data)
        
        self.assertEqual(data["error_code"], 405)
        self.assertEqual(data["message"], "method not allowed")
        self.assertEqual(data["success"], False)
        
    def test_search_for_questions(self):
        """
        Tests if questions which contain the search term are returned.
        """
        response = self.client().post('/questions/search', json={"searchTerm": "actor"})
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["current_category"])
        self.assertEqual(data["success"], True)
    
    def test_404_if_no_questions_match_search_term(self):
        """
        Tests if error 404 is thrown when no questions on te database match the search term
        """
        response = self.client().post('/questions/search', json={"searchTerm": "Nairobi"})
        data = json.loads(response.data)
        
        self.assertEqual(data["error_code"], 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
        
    def test_getting_questions_by_category(self):
        """
        Tests if questions are retrieved based on the selected category
        """
        response = self.client().get('/categories/2/questions')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["questions"])
        self.assertEqual(data["current_category"], 2)
        self.assertTrue(data["total_questions"])
        
    def test_404_if_category_does_not_exist(self):
        """
        Tests if a 404 error is thrown if the requested category of questions doesn't exist
        """
        response = self.client().get('/categories/100/questions')
        data = json.loads(response.data)
        
        self.assertEqual(data["error_code"], 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
        
    def test_422_for_wronglt_formatted_play_quiz_post_request(self):
        """
        Tests if an error 422 is returned for a wrongly formatted quiz request
        """
        response = self.client().post('/quizzes', json={"quiz_category":2,"previous_questions":[]})
        data = json.loads(response.data)
        
        self.assertEqual(data["error_code"], 422)
        self.assertEqual(data["message"], "unprocessable")
        self.assertEqual(data["success"], False)
        
                            
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()