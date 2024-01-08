# Backend

After cloning the backend to your local repository you need to perform the following steps, in order to start the flask application.

- Create a python environment in your backend directory:
  - (macOS and Windows): `python3 -m venv .venv` **or** `python -m venv .venv`
- Install all necessary dependencies with the provided requirements.txt file:
  - Change into the newly created virtual environment:
    - macOS and Windows: `cd .venv`
  - Activate the environment
    - macOS: `source bin/activate` <br>
    - Windows: `.\Scripts\Activate.ps1`
  - Install the required dependencies:
    - macOS: `pip install -r ../requirements.txt` <br>
    - Windows: `pip install -r ..\requirements.txt`
- Start the application:
  - Make sure you are in the `src` directory and your virtual environment is activated or the right python kernel is selected!
  - Run the following command to start the server in development mode:
    - macOS and Windows: `python3 app.py`
- In addition make sure to create or copy your `.env` file with your API keys to be able to use OpenAI and/or HuggingFace.
