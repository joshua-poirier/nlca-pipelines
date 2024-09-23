"""This is a simple CLI that demonstrates hot to use the library.

Typical usage example:
$ python -m data_access example
Running example command.
"""

# pylint: disable=fixme,line-too-long

import os

import click
import pandas as pd
from data_access.sources import GoogleDriveClient, S3Client

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
    bronze_pipeline = BronzePipeline(
        steps=[
            "serialize_rows",
            "add_source_name",
            "add_source_uri",
            "add_row_number",
            "add_source_updated_at",
            "add_id",
        ],
        options={
            "skiprows": 1,
            "source_created_at": google_drive_client.source_created_at,
            "source_name": google_drive_client.source_filename,
            "source_uri": google_drive_client.source_uri,
            "source_updated_at": google_drive_client.source_updated_at,
        },
    )
    bronze_df = bronze_pipeline.run(df=raw_df)

    # create and run silver pipeline
    silver_pipeline = SilverPipeline(
        steps=[
            "parse_json",
            "filter_missing",
            "eliminate_invalid_values",
            "impute_with_mean",
            "impute_with_mode",
            "sort",
        ],
        options={
            "cols_to_filter_missing": ["api10"],
            "cols_to_elim_invalid_values": [
                "direction",
                "welltype",
                "basin",
                "subbasin",
                "state",
                "county",
                "spuddate",
                "cum12moil",
                "cum12mgas",
                "cum12mwater",
            ],
            "cols_to_impute_with_mean": [
                "spuddate",
                "cum12moil",
                "cum12mgas",
                "cum12mwater",
            ],
            "cols_to_impute_with_mode": [
                "direction",
                "welltype",
                "basin",
                "subbasin",
                "state",
                "county",
            ],
            "cols_to_sort_by": ["api10"],
        },
    )
    silver_df = silver_pipeline.run(df=bronze_df)

    # save data to file
    if output_local:
        if not os.path.exists("data"):
            os.makedirs("data")
        silver_df.to_csv("data/" + output_filename, date_format="%Y-%m-%d")
    else:
        s3_client = S3Client()
        s3_client.write(df=bronze_df, bucket="nlca-bronze", filename=output_filename)
        s3_client.write(df=silver_df, bucket="nlca-silver", filename=output_filename)


if __name__ == "__main__":
    cli()
