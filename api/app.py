from api.config import app, login_manager
from api.blueprints.information import info_bp
from api.blueprints.authentication import auth_bp
from api.blueprints.dashboard import dash_bp
from api.blueprints.quiz_routes import quiz_bp
from api.blueprints.answering_quiz import taking_bp
from api.blueprints.resultsblueprint import results_bp
from api.blueprints.apiroutes import api_db
from models.user import User


@login_manager.user_loader
def load_user(user_id):
    """ Flask login user loader
    """
    return User.getByID(user_id)


app.register_blueprint(auth_bp)
app.register_blueprint(api_db)
app.register_blueprint(info_bp)
app.register_blueprint(dash_bp)
app.register_blueprint(quiz_bp)
app.register_blueprint(taking_bp)
app.register_blueprint(results_bp)


if __name__ == "__main__":
    app.run(debug=True)
