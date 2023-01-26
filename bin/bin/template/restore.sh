#!/bin/bash

# m4_ignore(
echo "This is just a script template, not the script (yet) - pass it to 'argbash' to fix this." >&2
exit 11  #)Created by argbash-init v2.8.0
# ARG_POSITIONAL_SINGLE([database], [Database])
# ARG_POSITIONAL_SINGLE([backup], [Backup archive (.zip) file path])
# ARG_HELP([<Backup odoo database and filestore>])
# ARGBASH_GO

# [ <-- needed because of Argbash

if [ ! -f $_arg_backup ]; then
  echo "Backup file \"$_arg_backup\" does not exist!"
  exit 1
fi

cmd="docker-compose run --rm -u root -v $_arg_backup:/tmp/backup.zip -v web_data:/var/lib/odoo web odoo-restore $_arg_database"

printf "\n"
echo $cmd
eval $cmd

# ] <-- needed because of Argbash
