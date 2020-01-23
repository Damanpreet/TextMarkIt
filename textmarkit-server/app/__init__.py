from app.blue import app

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

if __name__ == "__main__":
	app.run(debug=True)
