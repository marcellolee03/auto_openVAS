
#!/bin/bash


sudo -S docker cp scripts/CreateTarget/create-targets-from-host-list.gmp.py e38b91a3fb5a:/auto_vas/create-targets-from-host-list.gmp.py
sudo -S docker cp scripts/CreateTask/create-tasks-from-csv.gmp.py e38b91a3fb5a:/auto_vas/create-tasks-from-csv.gmp.py
sudo -S docker cp scripts/RunScan/start-scans-from-csv.py e38b91a3fb5a:/auto_vas/start-scans-from-csv.py
