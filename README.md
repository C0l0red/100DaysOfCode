# Django Email Sender
### Overview
This project is quite self explanatory.  
An email sender done with Django. Uses python-dotenv extension to get environment variables where you'd store your username and password.
An 'index.html' template for displaying the form to be used to take the details of the email and the recipient and a 'success.html' template to verify success./   

### How to use
 * Install Python for your operating system, info can be found at [Python.org](http://www.python.org)
 * Clone the repo using ```git clone <repo URL>``` in your directory of choice
 * Create a virtual environment with ```python -m venv venv``` on Windows or Mac, or ```python3 -m venv venv``` on Linux, and activate it using ```. venv/bin/activate``` on Mac or Linux or ```venv\Scripts\activate``` on Windows.(this is optional)
 * Install the requirements by entering ```pip install -r requirements.txt```
 * To set your email and password for Gmail, open the settings folder and create a '.env' file.
   * Inside it, enter ```EMAIL_HOST_USER=<your email>```. No spaces.
   * On the next line, ```EMAIL_HOST_PASSWORD=<your password>```. No spaces.
   * For any mail outside Gmail, please Google the Django settings for them.
 * Save it and start the server with ```python manage.py runserver``` on Windows or Mac, or ```python3 manage.py runserver``` on Linux.
 * Open the URL [localhost:8000/send](http://localhost:8000/send) in your browser.
 * Fill in the details, and that's it.

