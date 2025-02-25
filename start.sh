#!/bin/bash

str_to_bool() {
  case "$1" in
    [yY][eE][sS] | [yY] | [tT][rR][uU][eE] | [tT] | 1)
      return 0
      ;;
    [nN][oO] | [nN] | [fF][aA][lL][sS][eE] | [fF] | 0)
      return 1
      ;;
    *)
      return 1
      ;;
  esac
}

SERVER_PORT="${SERVER_PORT:-8198}"

python3 -m flask --app inventory-system init-db

if str_to_bool "$RESET_ON_RESTART"; then
  python3 -m flask --app inventory-system reset -y
elif str_to_bool "$CLEAR_DB_ON_RESTART"; then
  python3 -m flask --app inventory-system init-db -r
fi

python3 -m flask --app inventory-system ensure-admin

exec uwsgi --http :"$SERVER_PORT" --ini uwsgi.ini
