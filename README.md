# OpenGovSalary

Open Government Products ([OGP](https://www.open.gov.sg/)) maintains a list of their [products](https://www.open.gov.sg/products/) and the corresponding operational costs involved.
These costs include manpower costs, alongside a detailed breakdown of the contribution of each member.

This is great demonstration of transparency that I would like to commend.
Interestingly, this information is enough to form a system of linear equations in terms of each OGP employee's salary.
Should we find a good solution to this system of linear equations, we can approximate the salary of each employee.

### ⚠️ Disclaimer

Doing a cursory look through the output, there do seem to be some inaccuracies (e.g. a senior engineer with a much lower compensation than others).
Given that the senior engineer has much lower compensation than expected, it's likely that the other salaries are higher than the true amount.
Therefore, please only think of this project as a proof-of-concept meant to explore the idea of uncovering the salaries, but not results you can fully trust.

Building upon the good work of [lordidiot](https://github.com/lordidiot), the passage of time has unfortunately broken [his script](https://github.com/lordidiot/OpenGovSalary). This is my attempt at fixing it, alongside some cosmetic improvements.

## What this project is for

This project shows how public data can estimate pay bands. Person-level estimates are deliberately not published: this repository contains no per-person salary table and no per-person data files. If you run the code, the output stays on your machine in the gitignored `output/` directory.

## Set-up

- Install [poetry](https://python-poetry.org/docs/1.3#installing-with-the-official-installer) on your machine
- Install all project dependencies with `poetry install`
- Activate the project virtual environment by running the command `poetry shell`
- Run the command `uvicorn main:app --reload` to start the backend server on your machine. The server should be running on localhost:8000
- Optional: To view the Swagger UI of this application, visit localhost:8000/docs
- Note that due to the number of API calls to OGP, it could take up to 30 seconds to a minute to receive a successful response from the API
- Running `python contribution.py` writes its CSV to the gitignored `output/` directory, so it is never committed.
