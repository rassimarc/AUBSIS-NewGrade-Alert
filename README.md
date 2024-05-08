# Aub SIS New Grade Alert
This python script checks if a new grade was posted on the student's dashboard, by checking the number of credits every 30 mins.
It would then go on to send a notification to the phone of the user, every time a grade was released.
(Used to work before the introduction of 2FA to the institution)

## Installation Guide
1. First clone the repository
```bash
git clone https://github.com/rassimarc/AUBSIS-NewGrade-Alert.git
```

2. Install all the requirements
```bash
pip install -r requirements.txt
```

3. Add a .env file which contains the following
```env
USER_TOKEN=<Pushover User Token>
TOKEN=<Pushover App Token>
AUBSISID=<AUBSis Id>
PASSWORD=<AUBSis Password>
```

4. Run the app and enjoy! (PS: You can convert the app to an exe and put a shortcut in the startup folder for automatic grade checks)