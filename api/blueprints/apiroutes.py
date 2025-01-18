import re
from flask import Blueprint, request, jsonify
from math import ceil
from models import quizzesCollection


api_db = Blueprint('api_db', __name__)


@api_db.route('/get', methods=['GET'])
def getAll():
    """ Gets all quizzes from database
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
    """ Gets a quiz and returns it as json
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
