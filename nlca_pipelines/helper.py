# pylint: disable=missing-function-docstring

from data_access.sources import GoogleDriveClient

from .pipelines import BronzePipeline, SilverPipeline


def create_bronze_pipeline(google_drive_client: GoogleDriveClient) -> BronzePipeline:
    return BronzePipeline(
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


def create_silver_pipeline() -> SilverPipeline:
    return SilverPipeline(
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
