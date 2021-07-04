# GPW_collector
Warsaw Stock Exchange data collector and analyzer


source:
https://gist.github.com/mgeeky/b0e17a55c6a153fb7c34e897ad60ab3a

______________________________________

File: **money_pl_collector_xlsx.py ** version 1.0

description: This script collects data from Warsaw Stock Exchange (WSE) --- Giełda Papierów Wartościowych w Warszawie (GPW)
             and saves it in _Firm_Name_.xlsx file in _xls_files_ folder, for each company in WSE.
             If file is not exist then create it and add a data row, else just add row.
             
source: https://www.money.pl/gielda/spolki-gpw/

______________________________________

File: **wse_db_builder** version 1.0

description: this is script that builds database named _WSE_database_

______________________________________

File: **money_pl_collector_sql.py ** version 1.0

description: This script collects data from Warsaw Stock Exchange (WSE) --- Giełda Papierów Wartościowych w Warszawie (GPW)
             and saves it in _WSE_database_. 
             This required previouse creation of a database by **wse_db_builder** script
