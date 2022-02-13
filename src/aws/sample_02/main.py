import traceback
from datetime import datetime
from pprint import pprint
from typing import Final

import boto3

FUNCTION_NAME: Final[str] = "aws/sample_02"

logs: list = []
sequence: int = 0


def main() -> None:
    global logs, sequence  # Redeclare global variables

    try:
        logs.append({"message": f"[{(sequence := sequence + 1)}] === main Start ==="})

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#client
        logs.append({"message": f"[{(sequence := sequence + 1)}] S3へ接続"})
        s3 = boto3.client("s3", region_name="ap-northeast-1")

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_buckets
        logs.append({"message": f"[{(sequence := sequence + 1)}] バケット一覧を取得"})
        response = s3.list_buckets()
        if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
            raise Exception("バケット一覧取得失敗")

        buckets = [bucket["Name"] for bucket in response["Buckets"]]
        logs.append(
            {
                "message": f"[{(sequence := sequence + 1)}] display Buckets",
                "buckets": buckets,
            }
        )

        bucket_name = f"python-test-{datetime.now().strftime('%Y%m%d')}"
        logs.append({"message": f"[{(sequence := sequence + 1)}] display bucket_name", "bucket_name": bucket_name})

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_bucket
        if bucket_name in buckets:
            logs.append({"message": f"[{(sequence := sequence + 1)}] バケットを削除", "bucket_name": bucket_name})
            response = s3.delete_bucket(Bucket=bucket_name)
            if response["ResponseMetadata"]["HTTPStatusCode"] != 204:
                raise Exception("バケット削除失敗")
    except Exception as ex:
        logs.append(
            {"status": -1, "message": f"[{(sequence := sequence + 1)}] {ex}", "stackTrace": traceback.format_exc()}
        )
    finally:
        logs.append({"message": f"[{(sequence := sequence + 1)}] === main End ==="})


if __name__ == "__main__":
    logs.append({"message": f"[{(sequence := sequence + 1)}] === {FUNCTION_NAME} Start ==="})
    main()
    logs.append({"message": f"[{(sequence := sequence + 1)}] === {FUNCTION_NAME} End ==="})

    # ログ表示
    pprint("=== 実行ログ ===")
    pprint(logs)
