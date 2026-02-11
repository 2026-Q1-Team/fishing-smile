import logging
_logger = logging.getLogger(__name__)
from pathlib import Path

import click
import pandas as pd
import uvicorn

from fishing_smile.core.cast_net import cast_net as core_cast_net


@click.group('fishing-smile')
def cli():
    """Tools for anti-phish training"""
    pass


@cli.command()
@click.argument(
    'targets_csv_file',
    type = click.Path(
        exists = True,
        dir_okay = False,
        path_type = Path,
    ),
)
def cast_net(targets_csv_file):
    """Send out simulated phishing emails to targets"""
    targets = pd.read_csv(
        targets_csv_file,
        usecols = ['email', 'name_th', 'name_en'],
    )
    return core_cast_net(targets.itertuples())


@cli.command()
def deploy_fykes():
    """Start server handling interactions from phish targets.

    Endpoints created depends on what on-going attacks needs. For example,

    \b
    - tracking interaction
    - or serving next-stage payload
    """
    # TODO: Add option to serve only specific attack schemes.
    uvicorn.run(
        'fishing_smile.core.fyke_hub:app',
        host = '0.0.0.0',
        port = 8000,
        # TODO: disable reload in production
        reload = True,
        reload_dirs = ['/opt/app/src'],
    )


def main():
    logging.basicConfig(
        format = '%(asctime)s %(name)s %(levelname)s: %(message)s',
        level = logging.INFO,
    )
    cli()
