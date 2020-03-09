from app.blue import app
from app.config import cfg

# load environment
from dotenv import load_dotenv
load_dotenv('.env')

app.secret_key = cfg.SECRET_KEY 
app.config['SESSION_TYPE'] = cfg.SESSION_TYPE

if __name__ == "__main__":
	app.run(debug=True)
