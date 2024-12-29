PROJECT:
TODO: Makefile commands (ruff check, format, etc)
TODO: Ruff github integration Lint + Formatter
TODO: Create sqlite db at startup + migrations if not created. (????)
TODO: Dependabot
TODO: Alembic naming convention -> https://github.com/zhanymkanov/fastapi-best-practices?tab=readme-ov-file#migrations-alembic
BACKEND:
TODO: Code coverage
TODO: CLI for products (Click/Typer)
TODO: CORS for frontend.

    Product Service:
    TODO: schemas -> class ProjectBase(DispatchBase):
    id: Optional[PrimaryKey] ????

/////////// THIS ONE TO DO FIRST ///////////////
    TODO: Product Update instead of Product Replace
    TODO: Tests for each service function should query test database to see if operation was performed properly: https://github.com/igorbenav/fastcrud/blob/main/tests/sqlalchemy/crud/test_get.py
///////////////////////////////////////////////
    API:
    TODO: CRUD with tests
    TODO: assert_called_once_with() -> find a way to access db: DbSession (test_routes.py)
    TODO: assert_called_once_with() -> in test_service.py
    TODO: Ensure HTTP_204 is returned on successful delete request

FRONTEND:
TODO: Ensure client code from openapi schema is generated. (API for Items needs to be finished) (https://github.com/fastapi/full-stack-fastapi-template/blob/master/scripts/generate-client.sh)
https://github.com/luchog01/minimalistic-fastapi-template/tree/main