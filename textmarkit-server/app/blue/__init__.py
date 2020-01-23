from flask import Flask
app = Flask(__name__, instance_relative_config=True)#, template_folder='/site/templates')

#from site.routes import mod
#from api.routes import api_bp
from app.blue.site.routes import mod
from app.blue.api.routes import api_bp

app.register_blueprint(mod)

app.register_blueprint(api_bp, url_prefix='/api')

from flask import render_template
@app.route('/read_file')
def homepage():
    # list_example = ['Alvin', 'Simon', 'Theodore']
    # return render_template('base1.html', list_example=list_example)
    return render_template('base.html')