# UserGroups

## Commands

Installing requirements:

```bash
pip install -r requirements-dev.txt --force
```
Starting uvicorn:

```bash
uvicorn main:app --env-file environment.txt --reload
```
Running tests:
```bash
pytest --cov-report term-missing --cov=gql_ug tests
```
Cockroach:
```bash
docker exec -it roach1 ./cockroach --host=roach1:26357 init --insecure
docker exec -it roach1 ./cockroach sql --host=roach2:26258 --insecure
```