# LockerRoom
The LockerRoom app for Grant's Gym - CS601 Final Project

This is a web applications for members of the LockerRoom a premier home gym club hosted at Grant's Gym. The app is built from the ground up using flask with HTML/CSS/Javascript
on the front-end. This app will display the amazing equipment available at Grant's gym as well as allow users to sign up and great and account. The useres will be able to 
set goals, track their progress and eventually message each other on a message board.

## Code Style
- <a href="https://www.python.org/dev/peps/pep-0008/">PEP 8</a> (Python Enhancement Proposals)
## Core Features
The primary purpose of this app is to serve as the final project for BU CS601: Web App Development. As such the primary focus was creating custom HTML pages and writing my own CSS for stylization and Javascript for user input and data validation. In it's current phase it simply display's compentency with HTML/CSS/Javascript for the purpose of completing the requiremnts for the CS601 project. However once the course has endined this will be updated so that it is a fully usable gym app for the members of grants gym. In additon to the Front-End framworks this web app is build on Flask running Python code in the Back-End. This allows compatibility with a database so that user's can expect the following features:
   1. Create an Account
   2. Track Progress (weight,PRs,etc.)
   3. Message other members (Future)
   4. 

## Technology and Frameworks
- IDE: Visual Studio Code
- Front-end framework: jQuery/JavaScript/Bootstrap
- Back-end framework: Flask
- Version Control: Github

## Setup and Running
To use this app:-
1. Clone the app into a directory of your choice
2. Create a fresh virtual environment with no packages installed
   First from the terminal/command line navicate to the source where you have save the directory and type: py -m venv venv
3. Activate the new virtual environment you just created: 
        Windows: $source venv\Scripts\activate
        Linux/Mac: $source venv/bin/activate
4. Run the command - py -m pip install -r requirements.txt
5. With the venv active and the requirments installed run the app by typing flask run.
      ex) (venv) C:\Users\tomoc\Desktop\CS789>flask run
6. Navigate to the Localhost webserver (http://127.0.0.1:5000/) and begin using the app
