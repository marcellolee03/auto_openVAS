
#!/bin/bash


sudo -S docker exec -it greenbone-community-edition-gvmd-1 mkdir -p autovas
sudo -S docker cp scripts/CreateTarget/create-targets-from-host-list.gmp.py 5e0311da9783:/auto_vas/create-targets-from-host-list.gmp.py
sudo -S docker cp scripts/CreateTask/create-tasks-from-csv.gmp.py 5e0311da9783:/auto_vas/create-tasks-from-csv.gmp.py
sudo -S docker cp scripts/RunScan/start-scans-from-csv.py 5e0311da9783:/auto_vas/start-scans-from-csv.py
