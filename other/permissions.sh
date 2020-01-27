chown -R root:www-data /home/ex4d4_project
chmod -R 750 /home/ex4d4_project
find /home/ex4d4_project -type f -print0|xargs -0 chmod 740
chmod -R 770 /home/ex4d4_project/ex4d4/ex4d4/media
find /home/ex4d4_project/ex4d4/ex4d4/media -type f -print0|xargs -0 chmod 760
chmod 770 /home/ex4d4_project/ex4d4/logs
chmod -R 760 /home/ex4d4_project/ex4d4/logs/*
chmod 770 /home/ex4d4_project/ex4d4
chmod -R 760 /home/ex4d4_project/ex4d4/db.sqlite3