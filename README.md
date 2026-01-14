# StudentOrganizationSupportApplication
Application supporting students' daily work

# Table of content

- [Project set up for devs](#set-up-for-developers)
- [Application installation](#application-installation-for-users)
- [Application appearance](#application-appearance)

# Set up for developers
1. Download and install interpreter for `Python 3.13.0` from: `https://www.python.org/downloads/`.
2. Clone git repository using following command: 

```bash 
  git clone https://github.com/SOSA-Project/StudentOrganizationSupportApplication.git
```

3. Enter into `.\StudentOrganizationSupportApplication\` directory.
4. Create virtual environment for Python using command below:

```bash
  py -3.13 -m venv .venv
```

5. Activate virtual environment using command bellow:
- For Windows users: 

```bash
    . .\venv\Scripts\Activate.ps1
```

- For Linux users:
```bash
    . ./venv/Scripts/activate
```

6. Install required libraries (after virtual venv activation):

```bash
  pip install -r .\requirements.txt 
```

7. Run application using: 
```bash
  python run.py
```

or

- Using IDE (for PyCharm you can use `Shift + F10` keyboard shortcut)

## Tips

- For Windows users:

- After first configuration you can use `code_check.ps1` 
script which can activate virtual environment and improve 
your code format style into PEP8 using following command (only for Windows users):

```bash
  . .\code_check.ps1
```

- This script will give you feedback about your code and improve it automatically.


- For Unix users:
- Paste following commands in CLI:

```text
python -m mypy .\app\ --ignore-missing-imports
```

```text
python -m black --line-length 120 .\app\
```

```text
python -m flake8 .\app\ --max-line-length 120
```

# Application installation for users

- For Windows users:
- Application can be installed using a wizard, to do so follow the instructions below:

1. Enter the catalog: `./app_installer`
2. Double-click on the file `mysetup.exe`
3. Complete the installation process

- Application should install correctly on your computer

# Application appearance

- Sample screenshots form application:


- Login and registration process into application:
![Login](%20sample_screenshots/login_register_window.PNG)


- Calendar view:
![Calendar](%20sample_screenshots/calendar_view.PNG)


- Notifications view:
![Notifications](%20sample_screenshots/notifications_view.PNG)


- Notes view:
![Notes](%20sample_screenshots/notes_view.PNG)


- Grades view:
![Grades](%20sample_screenshots/grades_view.PNG)


- Average view:
![Average](%20sample_screenshots/average_view.PNG)


- Chat view:
![Chat](%20sample_screenshots/chat_view.PNG)


- Settings view:
![Settings](%20sample_screenshots/settings_view.PNG)


- White application theme:
![White](%20sample_screenshots/white_gui.PNG)