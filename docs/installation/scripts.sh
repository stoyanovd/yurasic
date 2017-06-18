

sudo -u postgres createuser yurasic_user
sudo -u postgres createdb yurasic
sudo -u postgres psql -c "ALTER USER yurasic_user PASSWORD '12345';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE yurasic TO yurasic_user;"


sudo -u postgres psql -c "\l"