# Releasing the IE-CoR clld app

```shell
git clone https://github.com/clld/cobl2
cd cobl2
pip install -e .[test]
```

```shell
clld initdb development.ini --cldf ../iecor-cldf/cldf/cldf-metadata.json
```

Store the tested requirements:
```shell
pip freeze > requirements.txt
```

Store a db dump:
```shell
pg_dump -xO iecor > iecor.sql
zip iecor.sql.zip iecor.sql
rm iecor.sql
```
