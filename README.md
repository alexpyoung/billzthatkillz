# Billz That Killz
Rudimentary analysis of bank and credit card statements

## Usage
```
mkdir -p pdf
cp path/to/pdfs ./pdf
docker-compose up app
```

## Development
### Static Analysis
```
docker-compose up ci
```

### REPL
```
docker-compose run app ipython
...
In [1]: import main
```
