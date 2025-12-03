# StudentOrganizationSupportApplication
Application supporting students' daily work

# Table of content

- [Project set up for devs](#set-up-for-developers)

# Set up for developers
1. Download and install interpreter for `Python 3.13.0` from: `https://www.python.org/downloads/`.
2. Clone git repository using following command: 

```bash 
  git clone https://github.com/SOSA-Project/StudentOrganizationSupportApplication.git
```

3. Enter into `.\StudentOrganizationSupportApplication\` directory.
4. Create virtual environment for Python using command below:

```bash
  py -3.13 -m venv venv
```

5. Activate virtual environment using command bellow:
- For Windows users: 

```bash
    . .\venv\Scripts\Activate.ps1
```

- For Linux users:
```bash
    . .\venv\Scripts\activate
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