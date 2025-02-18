import enum
from enum import Enum
import os

from src.shared.domain.repositories.challenge_repository_interface import IChallengeRepository


class STAGE(Enum):
    DOTENV = "DOTENV"
    DEV = "DEV"
    HOMOLOG = "HOMOLOG"
    PROD = "PROD"
    TEST = "TEST"


class Environments:
    """
    Defines the environment variables for the application. You should not instantiate this class directly. Please use Environments.get_envs() method instead.

    Usage:

    """
    stage: STAGE
    s3_bucket_name: str
    region: str
    endpoint_url: str = None
    dynamo_table_name: str
    dynamo_partition_key: str
    dynamo_sort_key: str
    cloud_frontget_Challenge_presenter_distribution_domain: str
    mss_name: str 

    def _configure_local(self):
        from dotenv import load_dotenv
        load_dotenv()
        os.environ["STAGE"] = os.environ.get("STAGE") or STAGE.DOTENV.value

    def load_envs(self):
        if "STAGE" not in os.environ or os.environ["STAGE"] == STAGE.DOTENV.value:
            self._configure_local()

        self.stage = STAGE[os.environ.get("STAGE")]
        self.mss_name = os.environ.get("MSS_NAME")
        
        if self.stage == STAGE.TEST:
            self.s3_bucket_name = "bucket-test"
            self.aws_access_key_id = "test-access-key"
            self.aws_secret_access_key = "test-secret-key"
            self.region = "sa-east-1"
            self.endpoint_url = "http://localhost:8000"
            self.dynamo_table_name = "user_mss_template-table"
            self.dynamo_partition_key = "PK"
            self.dynamo_sort_key = "SK"
            self.cloud_front_distribution_domain = "https://d3q9q9q9q9q9q9.cloudfront.net"
            self.sender_email = "test-sender@example.com"
            self.receiver_email = "test-receiver@example.com"
            self.image_key = "test-image-key"
            self.bucket_name = "test-bucket"
        else:
            self.s3_bucket_name = os.environ.get("S3_BUCKET_NAME")
            self.aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
            self.aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
            self.region = os.environ.get("REGION")
            self.endpoint_url = os.environ.get("ENDPOINT_URL")
            self.dynamo_table_name = os.environ.get("DYNAMO_TABLE_NAME")
            self.dynamo_partition_key = os.environ.get("DYNAMO_PARTITION_KEY")
            self.dynamo_sort_key = os.environ.get("DYNAMO_SORT_KEY")
            self.cloud_front_distribution_domain = os.environ.get("CLOUD_FRONT_DISTRIBUTION_DOMAIN")
            self.sender_email = os.environ.get("SENDER_EMAIL")
            self.receiver_email = os.environ.get("RECEIVER_EMAIL")
            self.image_key = os.environ.get("IMAGE_KEY")
            self.bucket_name = os.environ.get("BUCKET_NAME")


    @staticmethod
    def get_user_repo() -> IChallengeRepository:
        if Environments.get_envs().stage == STAGE.TEST:
            from src.shared.infra.repositories.challenge_repository_mock import ChallengeRepositoryMock
            return ChallengeRepositoryMock
        elif Environments.get_envs().stage in [STAGE.DEV, STAGE.HOMOLOG, STAGE.PROD]:
            from src.shared.infra.repositories.challenge_repository_dynamo import ChallengeRepositoryDynamo
            return ChallengeRepositoryDynamo
        else:
            raise Exception("No repository found for this stage")

    @staticmethod
    def get_envs() -> "Environments":
        """
        Returns the Environments object. This method should be used to get the Environments object instead of instantiating it directly.
        :return: Environments (stage={self.stage}, s3_bucket_name={self.s3_bucket_name}, region={self.region}, endpoint_url={self.endpoint_url})

        """
        envs = Environments()
        envs.load_envs()
        return envs

    def __repr__(self):
        return self.__dict__

