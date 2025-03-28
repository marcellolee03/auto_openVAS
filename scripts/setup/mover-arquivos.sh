
#!/bin/bash


sudo -S docker cp scripts/CreateTarget/create-targets-from-host-list.gmp.py 1987a0c0c04b:/auto_vas/create-targets-from-host-list.gmp.py
sudo -S docker cp scripts/CreateTask/create-tasks-from-csv.gmp.py 1987a0c0c04b:/auto_vas/create-tasks-from-csv.gmp.py
sudo -S docker cp scripts/RunScan/start-scans-from-csv.py 1987a0c0c04b:/auto_vas/start-scans-from-csv.py
