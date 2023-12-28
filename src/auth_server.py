from flask import Flask, request
import os

# Create a new Flask application instance
app = Flask(__name__)
# Define a route '/callback' which will handle the callback from Spotify OAuth 
@app.route('/callback')
def callback():
    code = request.args.get('code')
    # Check if the 'code' parameter is present
    if code:
		# If 'code' is present, write it to a file named 'auth_code.txt'
        with open('auth_code.txt', 'w') as file:
            file.write(code)
             # Return a response indicating that the authorization was successful
        return 'Authorization successful!'
    else:
        return 'Authorization failed.'

def run_server():
	# Retrieve the port number from an environment variable, defaulting to 8888 if not set
    port = os.getenv('FLASK_PORT', 8888)
    # Start the Flask application on the specified port
    app.run(port=port)
# Check if this script is the main program and not an imported module
if __name__ == '__main__':
    run_server()
