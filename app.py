from flask import Flask, render_template
from config import Config, BASE_DIR
from extensions import db
from models.user import User
from routes.auth import auth
from routes.dashboard import dashboard_bp
from routes.upload import upload_bp
from routes.analysis import analysis_bp
from routes.charts import charts_bp
from routes.ai import ai_bp
from routes.report import report_bp
from routes.ai_chat import ai_chat_bp
from routes.recommendation import recommendation_bp
from routes.cleaning import cleaning_bp
from routes.dashboard_stats import dashboard_stats_bp
from routes.chart_builder import chart_builder_bp
from routes.export import export_bp
from routes.profile import profile_bp
from routes.ai_dashboard import ai_dashboard_bp
from routes.chat import chat_bp
from routes.prediction import prediction_bp
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from routes.chat_with_dataset import chat_dataset_bp

app = Flask(__name__)

app.config.from_object(Config)

# Initialize Database
db.init_app(app)

# Register Blueprints
app.register_blueprint(auth)
app.register_blueprint(dashboard_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(analysis_bp)
app.register_blueprint(charts_bp)
app.register_blueprint(ai_bp)
app.register_blueprint(report_bp)
app.register_blueprint(ai_chat_bp)
app.register_blueprint(recommendation_bp)
app.register_blueprint(cleaning_bp)
app.register_blueprint(dashboard_stats_bp)
app.register_blueprint(chart_builder_bp)
app.register_blueprint(export_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(ai_dashboard_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(prediction_bp)
app.register_blueprint(chat_dataset_bp)

# Create database tables
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__": 
    app.run(debug=True)