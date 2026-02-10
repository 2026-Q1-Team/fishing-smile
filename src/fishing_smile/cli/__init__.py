import logging
_logger = logging.getLogger(__name__)
from pathlib import Path

import click
import pandas as pd

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


def main():
    logging.basicConfig(
        format = '%(asctime)s %(name)s %(levelname)s: %(message)s',
        level = logging.INFO,
    )
    cli()
