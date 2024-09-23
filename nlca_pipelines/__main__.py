"""This is a simple CLI that demonstrates hot to use the library.

Typical usage example:
$ python -m data_access example
Running example command.
"""

# pylint: disable=fixme,line-too-long

import os
from typing import Any, Dict

import click
import pandas as pd
from data_access.sources import GoogleDriveClient, S3Client

from .helper import create_bronze_pipeline, create_silver_pipeline
from .pipelines import BronzePipeline, SilverPipeline


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
    # stream data into dataframe
    google_drive_client = GoogleDriveClient(
        io_options={
            "encoding": "utf-8",
            "header": 0,
            "dtype": str,
            "keep_default_na": False,
        }
    )
    google_drive_client.get_file_id(filename=input_filename)
    raw_df: pd.DataFrame = google_drive_client.read()

    # create and run bronze pipeline
    bronze_pipeline: BronzePipeline = create_bronze_pipeline(google_drive_client)
    bronze_df = bronze_pipeline.run(df=raw_df)

    # create and run silver pipeline
    silver_pipeline: SilverPipeline = create_silver_pipeline()
    silver_df = silver_pipeline.run(df=bronze_df)

    # save data to file
    io_opts: Dict[str, Any] = {"date_format": "%Y-%m-%d", "index": False, "sep": "|"}
    output_filename = "data/" + output_filename
    if output_local:
        if not os.path.exists("data"):
            os.makedirs("data")
        silver_df.to_csv(output_filename, **io_opts)
    else:
        s3_client = S3Client(io_options=io_opts)
        s3_client.write(df=bronze_df, bucket="nlca-bronze", filename=output_filename)
        s3_client.write(df=silver_df, bucket="nlca-silver", filename=output_filename)


if __name__ == "__main__":
    cli()
