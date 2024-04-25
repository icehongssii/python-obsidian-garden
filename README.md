# python-obisidian-garden


- `#Static-Site-Generator`

- This project is python verision of [obsidian-garden](https://github.com/ecarrara/obsidian-garden), which is written in Rust


## How To Generate


```
poetry install
poetry shell
```

```
python ./src/main.py  build \
 						--vault "YOUR-VAULT-DIR-PATH" \
 						--template "YOUR-TEMPLATE-DIR-PATH" \
 						--output "YOUR-OUTPUT-DIR-PATH" \
 						--config "YOUR-CONTEXT.YAML" \
 						--domain "."
```

## How To Locally Test

```
cd YOUR-OUTPUT-DIR-PATH
python -m http.server 8000
```
then open your browser `localhost:8000/YOUR-PATH`