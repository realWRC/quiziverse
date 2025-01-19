"""
The Blueprint for API route used to expose quizzes.
"""

import re
from flask import Blueprint, request, jsonify
from math import ceil
from models import quizzesCollection


api_db = Blueprint('api_db', __name__)


@api_db.route('/get', methods=['GET'])
def getAll():
    """ 
    Retrieves all quizzes from database. Retrieves 30 quizzes by
    default, but can retrieve a maximum of 100 quizzes per
    request. The route supports pagination and you can specify
    the page and quizzes per page.

    Args:
        page(int): The page of the returned quizzes.
        per_page(int): The number of quizzes per page.
        search(str): The quiz title you are searching for.

    Response:
        JSON list of all quizzes in the database.

    Example usage:
        GET /get?page=1&per_page=5&search=food&action

        Respose: JSON list of 5 quizzes sorted by title which
        closely matches the search field of food
    """
    page = int(request.args.get('page', 1))
    if page <= 0:
        page = 1

    per_page = int(request.args.get('per_page', 30))
    if per_page > 100:
        per_page = 100
    if per_page <= 0:
        per_page = 30

    skip = (page - 1) * per_page
    query = request.args.get('search', '')

    pattern = re.compile(r'[^a-zA-Z0-9\s]')
    if pattern.search(query):
        query = re.escape(query)

    if query:
        total = quizzesCollection.count_documents(
            {"title": {"$regex": query, "$options": "i"}}
            )
        total_pages = ceil(total / per_page) if total > 0 else 1
        cursor = quizzesCollection.find(
            {"title": {"$regex": query, "$options": "i"}},
            {"_id": False, "creator_id": False},
            ).sort(
                [("title", 1), ("updated_at", 1)]
            ).skip(skip).limit(per_page)
        quizzes = list(cursor)
    else:
        total = quizzesCollection.count_documents({})
        total_pages = ceil(total / per_page) if total > 0 else 1
        cursor = quizzesCollection.find(
            {}, {'_id': False, 'creator_id': False}
        ).skip(skip).sort("updated_at", 1).limit(per_page)
        quizzes = list(cursor)

    if quizzes:
        return jsonify(quizzes)
    else:
        return jsonify({
            "message": "Not found"
        }), 500


@api_db.route('/get/<quiz_id>', methods=["GET"])
def get(quiz_id):
    """
    Retrieves a quiz from database using the given quiz_id. You
    can copy a quizzes quiz_id in the user interface.

    Args:
        quiz_id(str): Unique identifier of a quiz.

    Response:
        JSON list containing the quiz.

    Example usage:
        GET /get/34ed5fc9-5ffd-4696-b71f-21264162b87c

        Respose: JSON list containing a quiz the matches the
        quiz_id of 34ed5fc9-5ffd-4696-b71f-21264162b87c
    """
    cursor = quizzesCollection.find(
        {"quiz_id": quiz_id}, {"_id": False, "creator_id": False}
    )
    quiz = list(cursor)
    if not quiz:
        return jsonify({
            "message": "Quiz not found"
        }), 400

    return jsonify(quiz)
