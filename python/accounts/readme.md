# accounts

Hopefully I can automate some of this soon.

Remember : if I pay for something, it should be negative. Credit card transactions
are the other way around.

## process

- export files from bank for timeframes into data folder
- copy files to bnz_joint.csv, anz_personal.csv, anz_visa.csv
- move the original files to the archive sub folder
- import : go into accounts folder and run these `batch.sh` which has these three lines

```
python3 import_csv_bnz_joint.py ../../data/bnz_joint.csv
python3 import_csv_anz_personal.py ../../data/anz_personal.csv
python3 import_csv_anz_visa_.py ../../data/anz_visa.csv
```

- examine the results with queries #2 and #4 from the main_queries.sql file

If there are any without categories, use query #5 to add a category and then run

```
python3 update_categories.py
```

to pick them up.

- back up the database
