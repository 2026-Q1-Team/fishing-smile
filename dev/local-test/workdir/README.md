This directory is mounted inside `fishing_smile` containers to provide
persistent working directory. This also preserve python shell history.

Everything in this directory except this README.md file is untracked by git.

If this directory does not exist before running `docker compose up` then
workdir would be automatically created and owned by root user which can make it
inaccessible by running process. This README.md file exists mainly to make sure
the directory exist and owned by the working user.
