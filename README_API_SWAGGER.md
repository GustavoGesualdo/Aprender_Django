# API com Swagger

## Dependências

```bash
pip install -r requirements.txt
```

## Rodando o projeto

```bash
python manage.py migrate
python manage.py runserver
```

## Documentação

- Swagger UI: `/api/docs/`
- ReDoc: `/api/redoc/`
- OpenAPI Schema: `/api/schema/`

## Endpoints

- `GET/POST /api/criancas/`
- `GET/PUT/PATCH/DELETE /api/criancas/{id}/`
- `GET/POST /api/doadores/`
- `GET/PUT/PATCH/DELETE /api/doadores/{id}/`
