import logging
_logger = logging.getLogger(__name__)
from pathlib import Path

import click
import pandas as pd
import uvicorn
from sqlmodel import Session

from fishing_smile.settings import get_settings
from fishing_smile.database.engine import engine
from fishing_smile.database.init import initialize_database
from fishing_smile.core.model import *
from fishing_smile.core.cast_net import cast_net as core_cast_net


@click.group('fishing-smile')
def cli():
    """Tools for anti-phish training"""
    pass


@cli.command()
def init():
    """Initialize fishing_smile database"""
    initialize_database()


@cli.command()
@click.option(
    '--scheme', 'scheme_name',
    type = click.Choice(AttackScheme.list()),
    # TODO: Pick better default. Or make it required option?
    default = 'generic_org_change_password',
    help = 'Which attack scheme to use on targets',
)
@click.argument(
    'targets_csv_file',
    type = click.Path(
        exists = True,
        dir_okay = False,
        path_type = Path,
    ),
)
def cast_net(targets_csv_file, scheme_name):
    """Send out simulated phishing emails to targets"""
    targets = pd.read_csv(
        targets_csv_file,
        usecols = (lambda col: col in TargetProfile.model_fields and col != 'id'),
    )
    targets = [
        TargetProfile(**target._asdict())
        for target in targets.itertuples()
    ]
    scheme = AttackScheme.get(scheme_name)
    # TODO: try to place with get_session() ?
    with Session(engine) as session:
        core_cast_net(
            targets = targets,
            scheme = scheme,
            session = session,
        )


reload_option = click.option(
    '--reload',
    is_flag = True,
    help = 'Reload server when source code is modified. Useful for development.',
)


@cli.command()
@reload_option
def deploy_fykes(reload):
    """Start server handling interactions from phish targets.

    Endpoints created depends on what on-going attacks needs. For example,

    \b
    - tracking interaction
    - or serving next-stage payload
    """
    # TODO: Add option to serve only specific attack schemes.
    extra_args = {}
    if reload:
        extra_args.update(
            reload = True,
            reload_dirs = ['/opt/app/src'],
        )
    uvicorn.run(
        'fishing_smile.core.fyke_hub:app',
        host = '0.0.0.0',
        port = 8000,
        **extra_args,
    )


@cli.command()
@reload_option
@click.option(
    '--port',
    default = 8001,
    help = 'Port number for the server.',
)
def deploy_dashboard(reload, port):
    """Start Fish Eye server providing data for dashboards and external consumers."""
    extra_args = {}
    if reload:
        extra_args.update(
            reload = True,
            reload_dirs = ['/opt/app/src'],
        )
    uvicorn.run(
        'fishing_smile.core.db_hub:app',
        host = '0.0.0.0',
        port = port,
        **extra_args,
    )
     

def main():
    logging.basicConfig(
        format = '%(asctime)s %(name)s %(levelname)s: %(message)s',
        level = logging.INFO,
    )
    if get_settings().deployment_mode == 'development':
        logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
    cli()
