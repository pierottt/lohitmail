# lohitmail

## Setup

Install dependencies into the local Poetry virtualenv:

```powershell
python -m poetry install
```

The virtualenv is created at `.venv/`.

## Run

Add your Google service-account credentials as `credentials.json`, update
`.env`, then run one of these from the project root:

```powershell
python -m poetry run python -m interview.pass_interview
python -m poetry run python -m interview.fail_interview
python -m poetry run python -m form.pass_form
python -m poetry run python -m form.fail_form
```

`send_email.py` runs the interview-round rejection job, the same as
`python -m interview.fail_interview`.

`GMAIL_APP_PASSWORD` should be a Gmail app password, not your normal Gmail
password. Keep `DRY_RUN=true` until you are ready to send real emails.

The local `.env` file is ignored by Git. Use `.env.example` as the template if
you need to recreate it.

Non-secret application settings, campaign details, and sheet ranges are kept
in `config.py`.

## Structure

```text
lohitmail/
├── config.py
├── mailer.py
├── form/
│   ├── pass_form.py
│   └── fail_form.py
└── interview/
    ├── pass_interview.py
    └── fail_interview.py
```
