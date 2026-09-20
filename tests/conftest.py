import importlib
from unittest.mock import MagicMock

import pytest


@pytest.fixture
def lambda_handler_module(monkeypatch):
    """Import src.lambda_handler with DynamoDB access mocked out.

    EnvMonitor talks to DynamoDB at import time, so boto3.resource must be
    patched before the module (re)import happens.
    """
    monkeypatch.setenv("Region", "ap-northeast-1")
    monkeypatch.setenv("TableName", "m5_stickc_env_test")
    monkeypatch.setenv("PartitionKey", "id")
    monkeypatch.setenv("PartitionName", "env")

    fake_table = MagicMock()
    fake_table.get_item.return_value = {"Item": {"temperature": "25.3", "humidity": "48.2", "pressure": "1012.5"}}
    fake_dynamodb = MagicMock()
    fake_dynamodb.Table.return_value = fake_table
    monkeypatch.setattr("boto3.resource", MagicMock(return_value=fake_dynamodb))

    import src.env_monitor
    import src.lambda_handler

    importlib.reload(src.env_monitor)
    importlib.reload(src.lambda_handler)

    return src.lambda_handler
