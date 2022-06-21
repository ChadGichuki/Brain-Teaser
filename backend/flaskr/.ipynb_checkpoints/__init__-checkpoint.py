import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, all_questions):
    ''' Formats list of questions to be in pages of 10 questions each'''
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = []
    
    for question in all_questions:
        questions.append(question.format())
        
    questions_per_page = questions[start:end]
        
    return questions_per_page

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS')
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def obtain_categories():
        try:
            all_categories = Category.query.all()
            # Front-end expects categories to be a dictionary where {key=id:value=type}
            # Format returns a dictionary of each category eg{"id":1, "type":"science"}
            categories = {}
            for category in all_categories:
                category.format()
                categories.update({category.id: category.type})
            
            if len(all_categories) == 0:
                abort(404)
            else:
                return jsonify({
                    "categories": categories,
                    "success": True,
                    "status_code": 200
                }) 
        except:
            abort(422)
        
        
    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def obtain_questions():
        try:
            all_questions = Question.query.order_by(Question.id).all()
            questions = paginate_questions(request, all_questions)
            
            if len(questions) == 0:
                abort(404)
            
            all_categories = Category.query.all()
            categories = {}
            for category in all_categories:
                category.format()
                categories.update({category.id: category.type})
                
            return jsonify({
                "questions": questions,
                "total_questions": len(all_questions),
                # On request, let current category be the 1st in the dictionary
                "current_category": 1,
                "categories": categories,
                "success": True,
                "status_code": 200
            })
        except:
            abort(404)
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:quest_id>', methods=["DELETE"])
    def delete_question(quest_id):
        try:
            quest_to_delete = Question.query.filter(Question.id == quest_id).one_or_none()
            
            if quest_to_delete is None:
                abort(422)
            else:
                quest_to_delete.delete()
                
                return jsonify({
                    # No need to return anything else
                    "status_code": 200,
                    "success": True
                })
                
        except:
            abort(422)
            
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def add_new_question():
        body = request.get_json()
        
        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_difficulty = body.get("difficulty", None)
        new_category = body.get("category", None)
        
        try:
            question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)
            
            question.insert()
            
            return jsonify({
                # No need to return anything else
                "status_code": 200,
                "success": True
            })
        except:
            abort(422)
        
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=['POST'])
    def search_for_question():
        try:
            body = request.get_json()
            search_term = body.get("searchTerm", None)
            
            search = "%{}%".format(search_term)
            all_questions = Question.query.filter(Question.question.ilike(search)).all()
            
            if len(all_questions) == 0:
                abort(404)
                
            questions = []
    
            for question in all_questions:
                questions.append(question.format())
            
            #all_categories = Category.query.all()
            #categories = {}
            #for category in all_categories:
                #category.format()
                #categories.update({category.id: category.type})
            
            return jsonify({
                "questions": questions,
                "total_questions": len(all_questions),
                "current_category": 1,
                #"categories": categories
                "success": True,
                "status_code": 200
            })
        except:
            abort(404)
        
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    def get_categorised_questions(category_id):
        try:
            all_questions = Question.query.filter(Question.category == str(category_id)).all()
            
            if len(all_questions) == 0:
                abort(404)
            questions = paginate_questions(request, all_questions)
                
            all_categories = Category.query.all()
            categories = {}
            for category in all_categories:
                category.format()
                categories.update({category.id: category.type})
                
            return jsonify({
                "questions": questions,
                "total_questions": len(all_questions),
                "current_category": category_id,
                "success": True,
                "status_code": 200
            })
        
        except:
            abort(404)
        
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        try:
            body = request.get_json()
            previous_questions = body.get("previous_questions", None)
            quiz_category_dict = body.get("quiz_category", None)
            quiz_category = quiz_category_dict["id"]
            
            if quiz_category:
                all_questions = Question.query.filter(Question.category == quiz_category).all()
            else:
                all_questions = Question.query.all()
            
            print(all_questions)
            print("all: ", len(all_questions))
            print("prev: ", len(previous_questions))
            random_question = random.choice(all_questions)
            # Check if the question id is in the array of previous questions
            if random_question.id in previous_questions:
                if len(previous_questions) > len(all_questions):
                    return jsonify({"question": None})
                else:
                    random_question = random.choice(all_questions)
            else:
                question = random_question.format() 
            
            return jsonify({
                "question": question,
                "success": True,
                "status_code": 200
            })
        
        except:
            abort(422)
    
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error_code": 422,
            "message": "unprocessable"
        })
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error_code": 404,
            "message": "resource not found"
        })
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error_code": 405,
            "message": "method not allowed"
        })
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error_code": 400,
            "message": "bad request"
        })


    return app
