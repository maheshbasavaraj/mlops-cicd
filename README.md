# Class Project: CI/CD for a Machine Learning API using GitHub Actions

This is a 90-120 minute classroom project for final-year engineering students.

Students will build a tiny production-style ML project and automate quality checks using GitHub Actions.

## Learning Outcomes

By the end of the class, students should be able to explain and demonstrate:

- What CI/CD means for ML systems.
- Why ML pipelines need code tests and model quality gates.
- How GitHub Actions runs checks on every push and pull request.
- How to package a model API using Docker.
- Why a model should not be deployed only because the code compiles.

Official reference:
- GitHub Actions quickstart: https://docs.github.com/en/actions/get-started/quickstart
- Workflow syntax: https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax
- Publishing Docker images: https://docs.github.com/en/actions/tutorials/publish-packages/publish-docker-images

## Project Story

You are part of an MLOps team building a flower species prediction API.

The first data scientist created a model locally. Your task is to make the project production-ready:

1. Train the model reproducibly.
2. Test the model quality.
3. Test the API contract.
4. Build a Docker image.
5. Run everything automatically in GitHub Actions.

The project uses the built-in Iris dataset from scikit-learn, so no internet dataset download is needed.

## Project Structure

```text
mlops-ci-cd-class-project/
  .github/workflows/mlops-ci.yml
  src/
    app.py
    train.py
  tests/
    test_api.py
    test_model_quality.py
  Dockerfile
  requirements.txt
  README.md
```

## Teacher Flow

Use this order in class:

1. Run the model locally.
2. Run tests locally.
3. Show the GitHub Actions workflow file.
4. Push to GitHub and watch CI pass.
5. Ask students to intentionally break something.
6. Push again and watch CI fail.
7. Fix the project and watch CI pass again.
8. Discuss what this prevents in real production ML.

## Step 1 - Create a GitHub Repository

On GitHub:

1. Create a new repository, for example `mlops-ci-cd-iris-api`.
2. Keep it public or private as preferred.
3. Do not add a README on GitHub if you are pushing this folder as the initial project.

On your computer, from inside this project folder:

```bash
git init
git add .
git commit -m "Initial ML API with CI pipeline"
git branch -M main
#git remote add origin https://github.com/YOUR_USERNAME/mlops-ci-cd-iris-api.git
git remote add origin https://github.com/maheshbasavaraj/mlops-cicd.git
git push -u origin main
```

Then open the repository on GitHub and click the **Actions** tab.

## Step 2 - Install Dependencies Locally

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Step 3 - Train the Model

```bash
python src/train.py
```

Expected result:

- A model file is created at `artifacts/model.joblib`.
- The terminal prints test accuracy.
- Training fails if accuracy is below the threshold in `src/train.py`.

Discussion question:

> Why should a training script fail when quality is below a threshold?

## Step 4 - Run Tests

```bash
pytest
```

The tests check:

- The model reaches minimum accuracy.
- The API health endpoint works.
- The prediction endpoint returns a valid species name.

Discussion question:

> What is the difference between a code test and a model quality test?

## Step 5 - Run the API

```bash
uvicorn src.app:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

Try this prediction request:

```json
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
```

Expected prediction:

```json
{
  "species": "setosa"
}
```

## Step 6 - Build Docker Image

```bash
docker build -t iris-ml-api .
```

Run it:

```bash
docker run -p 8000:8000 iris-ml-api
```

Open:

```text
http://127.0.0.1:8000/docs
```

Discussion question:

> What problem does Docker solve in CI/CD?

## Step 7 - Understand the GitHub Actions Pipeline

The workflow is in:

```text
.github/workflows/mlops-ci.yml
```

It runs automatically on:

- Push to `main`
- Pull requests to `main`

It has two jobs:

1. `test`
   - Checks out the code.
   - Sets up Python.
   - Installs dependencies.
   - Runs `pytest`.

2. `docker-build`
   - Runs only after tests pass.
   - Builds the Docker image.

This is the core CI/CD idea:

```text
Code change -> automated tests -> model quality gate -> Docker build -> ready for deployment
```

## Step 8 - Student Challenge: Break the Pipeline

Ask students to make one of these changes:

Challenge A - Break the model quality gate:

In `src/train.py`, change:

```python
MIN_ACCURACY = 0.85
```

to:

```python
MIN_ACCURACY = 0.99
```

Commit and push. GitHub Actions should fail.

Challenge B - Break the API contract:

In `src/app.py`, change:

```
python
return {"species": species}
```

to:

```
python
return {"prediction": species}
```

Commit and push. API tests should fail.

Challenge C - Break Docker packaging:

In `Dockerfile`, change:

```dockerfile
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

to an invalid module path. Docker build or container startup will fail depending on the change.

## Step 9 - Student Challenge: Improve the Pipeline

Ask each team to add one improvement:

- Add `ruff` linting.
- Add a confusion matrix artifact.
- Add an MLflow tracking step.
- Add Docker image publishing to GitHub Container Registry.
- Add a deployment job that runs only when a GitHub Release is created.
- Add a `model_card.md` file and check that it exists in CI.

## Viva Questions

1. Why is CI/CD for ML harder than CI/CD for normal software?
2. What should happen if code tests pass but model accuracy drops?
3. Why should the Docker build run only after tests pass?
4. What is the difference between CI, CD, and CT in MLOps?
5. What production failure can be prevented by API contract tests?
6. What production failure can be prevented by data validation?
7. Should a model be deployed automatically after every training run? Why or why not?

## Assessment Rubric

Total: 20 marks

- 4 marks: Repository setup and clean commits.
- 4 marks: Training script runs and saves model.
- 4 marks: Tests pass locally and in GitHub Actions.
- 4 marks: Docker image builds successfully.
- 2 marks: Student can explain the workflow YAML.
- 2 marks: Student intentionally breaks and fixes one pipeline failure.

