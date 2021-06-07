from moto import mock_s3, mock_dynamodb2
import boto3, pytest, os


def mock_vault_objects_mapping():
    return {
        "socless_vault_tests.txt": "this came from the vault",
        "socless_vault_tests.json": '{"hello":"world"}',
    }


def setup_vault():
    """A helper function to instantiate the SOCless vault bucket with test files.
    This needs to be wrapped in moto's mock_s3 decorator before calling.
    Returns:
        boto3 s3 client
    """
    bucket_name = os.environ["SOCLESS_VAULT"]
    s3_client = boto3.client("s3")
    s3_client.create_bucket(Bucket=bucket_name)
    object_maps = mock_vault_objects_mapping()
    for key, content in object_maps.items():
        s3_client.put_object(Bucket=bucket_name, Key=key, Body=content)

    return s3_client


def setup_tables():
    """A helper function to instantiate SOCless dynamoDB tables.
    This needs to be wrapped in moto's mock_dynamodb2 decorator before calling.
    Returns:
        boto3 dynamodb client
    """
    dynamodb_client = boto3.client("dynamodb")

    tables_and_pkeys = {
        os.environ["SOCLESS_EVENTS_TABLE"]: "id",
        os.environ["SOCLESS_RESULTS_TABLE"]: "execution_id",
        os.environ["SOCLESS_DEDUP_TABLE"]: "dedup_hash",
        os.environ["SOCLESS_MESSAGE_RESPONSE_TABLE"]: "message_id",
    }

    for table_name, pkey in tables_and_pkeys.items():
        dynamodb_client.create_table(
            TableName=table_name,
            KeySchema=[{"AttributeName": pkey, "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": pkey, "AttributeType": "S"}],
        )

    return dynamodb_client


@pytest.fixture(scope="session", autouse=True)
def aws_credentials():
    """Mocked AWS Credentials for moto, auto runs in every test.
    Instantiate fake AWS Credentials that will be used to start up moto/boto3
    for tests. This fixture will be called by other fixtures to initialize
    their respective boto3 clients (s3, dynamodb, ssm, etc..) which are used for
    each each testing function that needs to interact with AWS.
    This fixture will also run automatically in every test to further prevent
    accidental live boto3 API calls.
    """
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"


@pytest.fixture(scope="session", autouse=True)
def setup_socless(aws_credentials):
    """Sets up a mock s3 bucket and dynamo tables in every test automatically.
    This uses moto's mock_s3 and mock_dynamodb2 decorators to instantiate
    SOCless vault s3 bucket and SOCless dynamoDB tables needed to run.
    This fixture is automatically run at the start of every test, and will
    wrap that test in the required moto decorators. Further boto3 calls can be
    made to the dynamodb and s3 clients in tests, other AWS clients will need
    their respective moto decorator (@mock_ssm, etc..) to function properly.
    """
    with mock_dynamodb2(), mock_s3():  # use moto decorators to mock boto3 calls
        # ensure boto3 is instantiated now, inside the decorators
        boto3.setup_default_session()

        setup_tables()
        setup_vault()

        yield
