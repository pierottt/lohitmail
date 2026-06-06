# lohitmail

## Setup

Install dependencies into the local Poetry virtualenv:

```powershell
python -m poetry install
```

The virtualenv is created at `.venv/`.

## Run

Add your Google service-account credentials as `credentials.json`, update
`.env`, then run one of these:

```powershell
python -m poetry run python pass_interview.py
python -m poetry run python fail_interview.py
python -m poetry run python pass_form.py
python -m poetry run python fail_form.py
```

`send_email.py` still works and runs the same job as `pass_interview.py`.

`GMAIL_APP_PASSWORD` should be a Gmail app password, not your normal Gmail
password. Keep `DRY_RUN=true` until you are ready to send real emails.

The local `.env` file is ignored by Git. Use `.env.example` as the template if
you need to recreate it.
