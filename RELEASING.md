# Releasing the IE-CoR clld app

```shell
git clone https://github.com/clld/cobl2
git clone --branch v1.2 --depth 1 https://github.com/lexibank/iecor
cd cobl2
pip install -e .[test]
```

```shell
clld initdb development.ini --cldf ../iecor/cldf/cldf-metadata.json
```

```shell
pytest
```

Store the tested requirements:
```shell
pip freeze > requirements.txt
```

Store a db dump:
```shell
pg_dump -xO --compress gzip:9 cobl2 > cobl2.sql.gz
```

