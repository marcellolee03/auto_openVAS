
#!/bin/bash

sudo -S docker cp scripts/CreateTarget/create-targets-from-host-list.gmp.py c5d36d62d503:/auto_vas/create-targets-from-host-list.gmp.py
sudo -S docker cp scripts/CreateTask/create-tasks-from-csv.gmp.py c5d36d62d503:/auto_vas/create-tasks-from-csv.gmp.py
sudo -S docker cp scripts/RunScan/start-scans-from-csv.py c5d36d62d503:/auto_vas/start-scans-from-csv.py
