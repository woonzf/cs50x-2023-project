# Your Personal Expense Tracker
### Video Demo: https://youtu.be/l83kys9yJJs
### Description:
This project is created as my CS50x 2023 final project. It is a web application that lets users to track their daily expenses. It uses **Flask** web framework to function, **SQLite** which is a light-weight relational database engine to store data and **Jinja**, a templating engine to pass data.

### Languages used:
- Python
- HTML
- CSS
- JavaScript

### Python modules required:
- cs50
- datetime
- flask
- flask_session
- werkzeug

### How to use:
#### If using the CS50 Codespace:
1. Change the directory to this project folder by entering the command below in the terminal.

        cd week10-project

1. Enter the command below in the terminal and **Ctrl + Left Mouse Click** the link provided to go to the web application.

        flask run

#### If using Visual Studio Code on your own device:
1. Make sure you have Python installed on your device. You can check if you have Python installed by entering the command below in the terminal. If not, follow this link for setup (https://www.geeksforgeeks.org/how-to-install-python-on-windows/).

        python --version

1. Make sure you have Python extension installed in your VS Code. Click the **Extensions** tab on the left side of VS Code window and search "Python". Install the one that is verified by **Microsoft**.
1. Open the project folder by clicking "**File**" on the top-left corner of the window and then "**Open Folder...**" and choose this project folder.
1. Follow this link to learn how to create a virtual environment in VS Code (https://code.visualstudio.com/docs/python/tutorial-flask).
1. Switch to **CMD** terminal, enter the command below and **Ctrl + Left Mouse Click** the link provided to go to the web application.

        flask run

### Features:
Firstly, it has a **Welcome** page that allows users to register or login. Then, it has a **Home** page that displays the expense summary of the user in the form of pie charts and a table, an **Expense** page that allows user to add expenses, a **History** page that allows user to view past expenses. It also has a **Settings** page that allows user to change their display name, preferred currency and password. Finally, it has a **Log Out** button that allows the user to log out.

### Files included:
#### Front End
In the **static** folder, it contains **Anurati.otf** which is used to display stylized-text on webpages, **favicon.ico** created with favicon.ico Generator (Link: https://www.favicon.cc/) which is the icon image on the webpage title, **CSS** files to format the layout of the webpages and **JS** files which contain scripts to prevent form resubmission, draw Google Pie Charts and functions for some buttons.

In the **templates** folder, it contains all the **HTML** files required to display the webpages properly.

#### Back End
In the root folder, it contains **app.py** which contains functions to setup the application, functions for all the routes/webpages mentioned and functions that setup global variables to be used in different routes. It also contains **helpers.py** which contains frequently-used functions in 'app.py'. **expense.db** is the database used to store all the data. Lastly, **requirements.txt** contains a list of modules required to run the project properly.

### Possible features / improvements to be added / made:
- Allow users to add their income.
- Improvement on the home page.
- Make the entire application mobile-friendly, currently only the welcome page is mobile-friendly.
- Make the password requirement more complex.
