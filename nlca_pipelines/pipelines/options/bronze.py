from typing_extensions import TypedDict


class BronzePipelineOptionsDict(TypedDict, total=False):
    """Enforces typing for the `options` used by the `BronzePipeline`.

    Attributes:
        skiprows (int): Number of rows to add to the row number.
        source_created_at (str): When the file was created.
        source_name (str): Filename of the input data.
        source_uri (str): The URI of the source (from web, Google Drive,
            S3, etc.).
        source_updated_at (str): When the file was last updated.
    """

    skiprows: int
    source_created_at: str
    source_name: str
    source_uri: str
    source_updated_at: str
