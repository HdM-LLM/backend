# Backend

## Using the backend for the first time

After cloning the backend to your local repository you need to perform the following steps, in order to start start the flask application.

<ol>
    <li>
        Create a python virtual environment (venv) in your backend directory:
        <ul>
            <li>
                (terminal): python3 -m venv .venv or python -m venv .venv
            </li>
        </ul>
    </li>
    <li>
        Install all necessary dependencies with the provided requirements.txt file:
        <ol>
            <li>
                Change into the newly created virtual environment:
                <ul>
                    <li>
                        (terminal): cd .venv
                    </li>
                </ul>
            </li>
            <li>
                Activate the enviroment
                <ul>
                    <li>
                        (terminal): source bin/activate<br>
                        or (windows cmd): .\Scripts\Activate.ps1
                    </li>
                </ul>
            </li>
            <li>
                Install the required dependencies:
                <ul>
                    <li>
                        (terminal): pip install -r ../requirements.txt
                        or (windows cmd): pip install -r ..\requirements.txt
                    </li>
                </ul>
            </li>
        </ol>
    </li>
    <li>
        Start the application:
        <ul>
            <li>
                <b>Make sure you are in the src directory and, that your virtual environment is activated or the right python kernel is selected!</b>
                (terminal): flask --app app run <br>
            </li>
        </ul>
    </li>
    <li>
        In addition make sure to create or copy your <b>.env file</b> to gain access to the apis of OpenAPI and/or Hugging Face.
    </li>
</ol>
