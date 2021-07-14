# accounts

Hopefully I can automate some of this soon.

Remember : if I pay for something, it should be negative. Credit card transactions
are the other way around.

## anz

## bnz

## process

- export files from bank for timeframes into data folder
- copy files to bnz_work.csv, bnz_joint.csv, anz_personal.csv, anz_visa.csv
- move the original files to the archive sub folder
- import : go into accounts folder and run `batch.sh` which has these four lines

```
python3 import_csv_bnz_joint.py ../../data/bnz_joint.csv
python3 import_csv_anz_personal.py ../../data/anz_personal.csv
python3 import_csv_anz_visa_.py ../../data/anz_visa.csv
python3 import_csv_bnz_work_.py ../../data/bnz_work.csv
```

- examine the results with queries #2 and #4 from the main_queries.sql file

If there are any without categories, use query #5 to add a category and then run

```
python3 update_categories.py
```

to pick them up.

- back up the database

```
pg_dump croesus > pg_dump_2021-07-14.sql
```
