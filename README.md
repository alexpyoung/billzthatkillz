# Billz That Killz
Rudimentary analysis of bank and credit card statements

## Usage
```
mkdir -p pdf
cp path/to/pdfs ./pdf
docker-compose run django python manage.py import_pdfs
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
