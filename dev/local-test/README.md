# Setup

## Prerequisite

The only prerequisite is **Docker Engine**.

- Linux user can [install Docker Engine](https://docs.docker.com/engine/install/) directly.
- Windows user can install Docker Engine through
  [Docker Desktop for Windows](https://docs.docker.com/desktop/setup/install/windows-install/)

## Deploy locally for testing

To deploy for local testing, open "this" directory and run:

```shell
docker compose up
```

Wait for a bit and all the servers should become online.

# Usage

## Accessing phpMyAdmin

Go to `http://localhost:8091` and use

- username: `fish_app`
- password: `db_password_for_local_test`

## Using the CLI

```shell
docker compose run --build --rm cli
```

For now, only `cast-net` command is available.
