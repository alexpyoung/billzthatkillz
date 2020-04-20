# Billz That Killz
Rudimentary analysis of bank and credit card statements

## Usage
```
mkdir -p pdf
cp path/to/pdfs ./pdf
docker-compose up
```

## Development
### pylint
```
docker-compose run app pylint .
```

### isort
```
docker-compose run app isort
```

### iPython
```
docker-compose run app ipython
```
