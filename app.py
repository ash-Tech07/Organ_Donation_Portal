from flask import Flask, render_template
app = Flask(__name__)


# Common app configs
# Cache control 
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

# 404 Error Page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('page_404.html'), 404


# Route configurations
from routes import routes
app.register_blueprint(routes)
