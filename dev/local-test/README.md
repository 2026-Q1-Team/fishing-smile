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

This will opens a shell into container installed with `fishing-smile` CLI
command. See `--help` for more info like this:

```shell
fishing-smile --help
```

## Updating dependency

The same CLI container also has `uv` package manager which you can use to manage
python dependencies without having to install `uv` outside of docker.
Here's how to add a new package, just run the following in the CLI shell.

```shell
# Go to the directory where `pyproject.toml` and `uv.lock` are mounted
cd /opt/app
uv add --no-sync PACKAGE
```

where `PACKAGE` should be replaced by the name of the package you want to add to
the dependencies list. After that, you should shutdown the CLI container and
rebuild it.
