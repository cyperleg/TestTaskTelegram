## Install dependences
```
pip install requirements.txt
```
## Start script
```
python main.py
```
The API can be found on http://127.0.0.1:8000 and docs on: http://127.0.0.1:8000/docs or http://127.0.0.1:8000/redoc
## Usage
- `/create` create user
- `/login` login in system for bearer token
- `/user/me` return your realisation from DB, required token
- `/user/set_api` link telegram account to user, required token
- `/user/auth` auth linked account, **important to use this BEFORE dialog usage** , required token
- `/user/dialog` returns dialogs by filter, required token and auth
## How to test
Simply use docs to test all functions
