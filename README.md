# Comp405-Inventory

#### *Currently in Development*

## How to Run
### Production
With Docker installed, use the [docker compose file](docker-compose.yaml).\
Be sure to set `MYSQL_PASSWORD` on both containers and `ADMIN_PASSWORD` for this container.

### Development

To completely recreate the database (add `-y` to override prompt):
```bash
flask --app inventory-system reset
```

Also take a look at the help menu for more commands:
```bash
flask --app inventory-system --help
```

Run the development server:
```bash
flask --app inventory-system --debug run
```
The frontend is now available at http://127.0.0.1:5000
