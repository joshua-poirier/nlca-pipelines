"""This is a simple CLI that demonstrates hot to use the library.

Typical usage example:
$ python -m data_access example
Running example command.
"""

# pylint: disable=fixme,line-too-long

import os

import click
import pandas as pd
from data_access.sources.google_drive import GoogleDriveClient


@click.group(name="cli")
def cli() -> None:
    """Click command group for the library."""


@cli.command(name="main")
@click.option(
    "--input-filename",
    required=True,
    type=click.STRING,
    help="Filename of input file (hosted by Google Drive)",
)
@click.option(
    "--output-filename",
    default="wells.csv",
    type=click.STRING,
    help="Filename for processed output file",
)
@click.option(
    "--output-local",
    is_flag=True,
    type=click.BOOL,
    help="If True, save the output file to local disk",
)
def main(input_filename: str, output_filename: str, output_local: bool) -> None:
    """Main entry-point for processing the input file.

    In the context of the coding assignment, this tackles the requirements relating to
    **Part 1**, covered in the
    [README](https://github.com/joshua-poirier/nlca-pipelines/tree/chore/project-skeleton).

    Attributes:
        input_filename (str): The filename for the input data, hosted in Google Drive.
        output_filename (str): The filename for the output data.
        output_local (bool): Whether to save the output file to local disk (True), or
            remotely on S3 (False).

    Examples:
        Launch the virtual environment
        $ pipenv shell

        # Run the application, outputting locally
        (nlca-pipelines) $ python -m nlca_pipelines main --input-filename "novi-data-engineer-assignment.csv" --output-local

        # Run the application, outputting remotely
        (nlca-pipeliens) $ python -m nlca_pipelines main --input-filename "novi-data-engineer-assignment.csv"
    """
    client = GoogleDriveClient(io_options={"encoding": "utf-8", "header": 0})
    client.get_file_id(filename=input_filename)

    # stream data into dataframe
    df: pd.DataFrame = client.read()
    df.head()

    # save data to file
    if output_local and not os.path.exists("data"):
        os.makedirs("data")
        df.to_csv("data/" + output_filename, date_format="%Y-%m-%d")
    else:
        # TODO: Write data to S3
        pass


if __name__ == "__main__":
    cli()
