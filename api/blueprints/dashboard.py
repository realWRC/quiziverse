import re
from api.config import year
from flask import Blueprint, flash, request, render_template, url_for, redirect
from flask_login import current_user
from math import ceil
from models.quiz import Quiz
from models import quizzesCollection, resultsCollection


dash_bp = Blueprint('dash', __name__)


@dash_bp.route("/home", methods=["GET", "POST"])
def home():
    """ Renders the users home page
    """
    if not current_user.is_authenticated:
        flash("You must be logged in first.")
        return redirect(url_for('auth.login'))

    page = int(request.args.get('page', 1))
    if page <= 0:
        page = 1

    per_page = 24
    # if per_page > 30:
    #     per_page = 30
    # if per_page < 30:
    #     per_page = 30

    skip = (page - 1) * per_page
    query = request.args.get('search', '')

    category = request.args.get('category', '')
    if category.lower() == "default" or category.lower() == '':
        category = None
    categories = ["title", "updated_at", "created_at"]
    valid_categories = ["title", "updated_at", "created_at", "default", None]
    if category not in valid_categories:
        flash("Invalid Sort Order")
        return redirect(url_for('dash.home', category=None))
    # categories = quizzesCollection.distinct("category")

    pattern = re.compile(r'[^a-zA-Z0-9\s]')
    if pattern.search(query):
        query = re.escape(query)

    def url_for_other_page(page):
        args = request.args.copy()
        args['page'] = page
        return url_for('dash.home', _external=False, **args)

    if query:
        total = quizzesCollection.count_documents(
            {"title": {"$regex": query, "$options": "i"}}
            )
        total_pages = ceil(total / per_page) if total > 0 else 1
        if category:
            cursor = quizzesCollection.find(
                {"title": {"$regex": query, "$options": "i"}}
                ).sort([(category, -1), ("updated_at", -1)]).skip(skip).limit(per_page)
        else:
            cursor = quizzesCollection.find(
                {"title": {"$regex": query, "$options": "i"}}
                ).sort([("title", 1), ("updated_at", 1)]).skip(skip).limit(per_page)
        quizzes = list(cursor)
        pagination = {
            'page': page,
            'total_pages': total_pages,
            'has_prev': page > 1,
            'has_next': page < total_pages,
            'prev_url': url_for_other_page(page - 1) if page > 1 else None,
            'next_url': url_for_other_page(page + 1) if page < total_pages else None,
        }
    else:
        total = quizzesCollection.count_documents({})
        total_pages = ceil(total / per_page) if total > 0 else 1
        if category:
            # cursor = Quiz.getAll().skip(skip).sort([(category, 1), ("updated_at", 1)]).limit(per_page)
            cursor = Quiz.getAll().sort(category, -1).skip(skip).limit(per_page)
        else:
            cursor = Quiz.getAll().sort([("title", 1), ("updated_at", -1)]).skip(skip).limit(per_page)
        quizzes = list(cursor)
        pagination = {
            'page': page,
            'total_pages': total_pages,
            'has_prev': page > 1,
            'has_next': page < total_pages,
            'prev_url': url_for_other_page(page - 1) if page > 1 else None,
            'next_url': url_for_other_page(page + 1) if page < total_pages else None,
        }

    return render_template(
        "home.html", title='dash.home',
        year=year, query=query,
        quizzes=quizzes, categories=categories,
        selected_category = category,
        pagination=pagination
    )


@dash_bp.route("/myquizzes", methods=["GET", "POST"])
def myquizzes():
    """ Shows all quizes created by a given user.
    """
    if not current_user.is_authenticated:
        flash("You must be logged in first.")
        return redirect(url_for('auth.login'))

    page = int(request.args.get('page', 1))
    if page <= 0:
        page = 1

    per_page = 24
    # if per_page > 30:
    #     per_page = 30
    # if per_page < 30:
    #     per_page = 30

    skip = (page - 1) * per_page
    query = request.args.get('search', '')

    category = request.args.get('category', '')
    if category.lower() == "default" or category.lower() == '':
        category = None
    categories = ["title", "updated_at", "created_at"]
    valid_categories = ["title", "updated_at", "created_at", "default", None]
    if category not in valid_categories:
        flash("Invalid Sort Order")
        return redirect(url_for('dash.home', category=None))

    pattern = re.compile(r'[^a-zA-Z0-9\s]')
    if pattern.search(query):
        query = re.escape(query)

    def url_for_other_page(page):
        args = request.args.copy()
        args['page'] = page
        return url_for('dash.myquizzes', _external=False, **args)

    if query:
        total = quizzesCollection.count_documents(
            {
                "creator_id": current_user.get_id(),
                "title": {"$regex": query, "$options": "i"}}
            )
        total_pages = ceil(total / per_page) if total > 0 else 1
        if category:
            cursor = quizzesCollection.find(
                {
                    "creator_id": current_user.get_id(),
                    "title": {"$regex": query, "$options": "i"}}
                ).sort([(category, -1), ("updated_at", 1)]).skip(skip).limit(per_page)
        else:
            cursor = quizzesCollection.find(
                {
                    "creator_id": current_user.get_id(),
                    "title": {"$regex": query, "$options": "i"}}
                ).sort([("title", 1), ("updated_at", -1)]).skip(skip).limit(per_page)
        quizzes = list(cursor)
        # quizzes = Quiz.searchUserQuizzes(current_user.get_id(),query)
        pagination = {
            'page': page,
            'total_pages': total_pages,
            'has_prev': page > 1,
            'has_next': page < total_pages,
            'prev_url': url_for_other_page(page - 1) if page > 1 else None,
            'next_url': url_for_other_page(page + 1) if page < total_pages else None,
        }
    else:
        total = quizzesCollection.count_documents({"creator_id": current_user.get_id()})
        total_pages = ceil(total / per_page) if total > 0 else 1
        if category:
            cursor = Quiz.getAllUserQuizzes(current_user.get_id()).sort(category, -1).skip(skip).limit(per_page)
        else:
            cursor = Quiz.getAllUserQuizzes(current_user.get_id()).skip(skip).sort("title", -1).limit(per_page)
        quizzes = list(cursor)
        pagination = {
            'page': page,
            'total_pages': total_pages,
            'has_prev': page > 1,
            'has_next': page < total_pages,
            'prev_url': url_for_other_page(page - 1) if page > 1 else None,
            'next_url': url_for_other_page(page + 1) if page < total_pages else None,
        }

    return render_template(
        "myquizzes.html",
        quizzes=quizzes,
        query=query,
        title="My Quizzes",
        year=year,
        categories=categories,
        selected_category = category,
        pagination=pagination
    )


@dash_bp.route('/myresults', methods=["GET", "POST"])
def myresults():
    """ Results page for all quizzes taken
    """
    if not current_user.is_authenticated:
        flash("You must be logged in first")
        return redirect(url_for('auth.login'))

    page = int(request.args.get('page', 1))
    if page <= 0:
        page = 1

    per_page = 24
    # if per_page > 30:
    #     per_page = 30
    # if per_page < 30:
    #     per_page = 30

    skip = (page - 1) * per_page
    query = request.args.get('search', '')

    pattern = re.compile(r'[^a-zA-Z0-9\s]')
    if pattern.search(query):
        query = re.escape(query)

    category = request.args.get('category', '')
    if category.lower() == "default" or category.lower() == '':
        category = None
    categories = ["title", "latest_attempt"]
    valid_categories = ["title", "latest_attempt", "default", None]
    if category not in valid_categories:
        flash("Invalid Sort Order")
        return redirect(url_for('dash.home', category=None))

    def url_for_other_page(page):
        args = request.args.copy()
        args['page'] = page
        return url_for('dash.myresults', _external=False, **args)

    if query:
        total = resultsCollection.count_documents(
            {
                "user_id": current_user.get_id(),
                "title": {"$regex": query, "$options": "i"}
            }
        )
        total_pages = ceil(total / per_page) if total > 0 else 1
        if category:
            cursor = resultsCollection.find(
                {
                    "user_id": current_user.get_id(),
                    "title": {"$regex": query, "$options": "i"}
                }
            ).sort([(category, -1), ("updated_at", -1)]).skip(skip).limit(per_page)
        else:
            cursor = resultsCollection.find(
                {
                    "user_id": current_user.get_id(),
                    "title": {"$regex": query, "$options": "i"}
                }
            ).sort([("title", 1), ("updated_at", -1)]).skip(skip).limit(per_page)
        results = list(cursor)
        # results = Result.searchMyResults(current_user.get_id(), query=query)
        pagination = {
            'page': page,
            'total_pages': total_pages,
            'has_prev': page > 1,
            'has_next': page < total_pages,
            'prev_url': url_for_other_page(page - 1) if page > 1 else None,
            'next_url': url_for_other_page(page + 1) if page < total_pages else None,
        }
    else:
        total = resultsCollection.count_documents({"user_id": current_user.get_id()})
        total_pages = ceil(total / per_page) if total > 0 else 1
        # results = Result.getQuizResult(current_user.get_id())
        # results = list(results) if results else None
        if category:
            cursor = resultsCollection.find({"user_id": current_user.get_id()}).sort(category, -1).skip(skip).limit(per_page)
        else:
            cursor = resultsCollection.find({"user_id": current_user.get_id()}).sort("title", -1).skip(skip).limit(per_page)
        results = list(cursor) if cursor else None
        pagination = {
            'page': page,
            'total_pages': total_pages,
            'has_prev': page > 1,
            'has_next': page < total_pages,
            'prev_url': url_for_other_page(page - 1) if page > 1 else None,
            'next_url': url_for_other_page(page + 1) if page < total_pages else None,
        }
    
    return render_template(
        "myresults.html",
        results=results,
        query=query,
        categories=categories,
        selected_category = category,
        pagination=pagination,
        year=year
    )
