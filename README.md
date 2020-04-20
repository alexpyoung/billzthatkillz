# Billz That Killz
Rudimentary analysis of bank and credit card statements

## Usage
```
mkdir -p pdf
cp path/to/pdfs ./pdf
docker-compose up app
```

## Development
### pylint
```
docker-compose up lint
```

### isort
```
docker-compose up sort
```

### iPython
```
docker-compose run app ipython
```
