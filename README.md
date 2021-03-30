# Billz That Killz

[![CI](https://github.com/alexpyoung/billzthatkillz/actions/workflows/main.yml/badge.svg)](https://github.com/alexpyoung/billzthatkillz/actions/workflows/main.yml)

Rudimentary analysis of bank and credit card statements

## Usage
```
docker-compose up -d django
open "http://localhost:8000/admin"
```

### Injesting new statements
```
mkdir -p pdf
cp path/to/pdfs ./pdf
docker-compose run --rm django python manage.py import_pdfs
```

## Development
### Static Analysis
```
docker-compose up ci
```

### REPL
```
docker-compose run django python manage.py shell
```
