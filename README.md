# Comp405-Inventory

#### *Currently in Development*

## How to Run
### Development
Initialize the database (add `-r` to hard reset):
```
flask --app inventory-system init-db
```

To create an admin user from the dev config with username `root` and password `password`:
```
flask --app inventory-system ensure-admin
```
or to create a custom admin user:
```
flask --app inventory-system create-admin
```

Run the development server:
```
flask --app inventory-system --debug run
```
The frontend is now available at http://localhost:5000


### Production
Use the [docker compose file](docker-compose.yaml).\
Be sure to set `MYSQL_PASSWORD` on both containers and `ADMIN_PASSWORD` for this container.
