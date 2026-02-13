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

# Config

## SMTP account

### Google account with 2-Step Verification enabled.

+ Setting up a Google account. Step-by-step guide [here](https://support.google.com/accounts/answer/27441).
+ Enabling 2-Step Verification on your Google account. Step-by-step
  guide [here](https://support.google.com/accounts/answer/185839).

### Creating a Google account App password.

An app password is required for sending emails through Google SMTP servers.

+ Open your [Google account security menu](https://myaccount.google.com/security).
+ Locate and click the **2-Step-Verification** option.
+ Locate and click the **App passwords** option.
+ Enter a name into the **App name** field.
+ Click the **Create** button.
+ Copy the new app password and store it somewhere safe.

### Using the Google account App password.

In ``/dev/local-test/env/local-test.env``, locate entry:

```
FISHING_SMILE_CAST_SENDER='%EMAIL'
FISHING_SMILE_CAST_PASSWORD='%PASSWORD'
```

Replace ``%EMAIL`` & ``%PASSWORD`` with your Google account email address and app password.

**IMPORTANT** : This method limits the amount of emails that can be sent to 2,000 emails per day according
to [this](https://support.google.com/a/answer/176600) Google support article.

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

## Run automated test

To run all tests via pytest,
go into CLI container shell and run:

```shell
pytest ..

# Or if current directory has been changed,
# give location of pyproject.toml explicitly.
pytest /opt/app
```

