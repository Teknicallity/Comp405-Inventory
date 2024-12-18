# Comp405-Inventory

***Developed for Intro to Databases Systems Course***

This project is designed to manage inventory within a workshop environment. 
It provides a structured system to track items, employees, and checkouts, while also offering easy access to 
documentation through QR codes. The system includes an item list for monitoring item details, locations, and statuses, 
a checkout list for recording who borrowed what and when, and a documentation list for managing important information 
related to each item.

## Features
- Item List: Tracks item details, location, and status.
- Checkout List: Records who checked out items and when they were returned.
- Employee List: Keep track of leaders and who reports to who.
- Documentation List: Manages important documentation associated with each item.
- QR Code Integration: Provides quick access to item and document pages via QR codes.

## How to Run
### Production
With Docker installed, use the [docker compose file](docker-compose.yaml).\
Be sure to set `MYSQL_PASSWORD` on both containers and `ADMIN_PASSWORD` for this container.

[Comp405-Inventory on Dockerhub](https://hub.docker.com/r/teknicallity/comp405-inventory)

### Development

Create a python virtual environment and install dependencies:
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

The program looks for a default MySQL database at `localhost:3306` with user `root` and password `password`.
To change this, edit [config/dev.py](config/dev.py).

To completely recreate the database instance (add `-y` to override prompt):
```bash
flask --app inventory-system reset
```
This will create employees and their respective user accounts defined in [employees.csv](./employees.csv)

Also take a look at the help menu for more commands:
```bash
flask --app inventory-system --help
```

Run the development server:
```bash
flask --app inventory-system --debug run
```
The frontend is now available at http://127.0.0.1:5000

## Technologies Used
- Backend: Flask
- Database: MySQL
- Containerization: Docker
- Frontend: Bootstrap