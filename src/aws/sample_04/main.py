import traceback
from datetime import datetime
from pprint import pprint
from typing import Final

import boto3

FUNCTION_NAME: Final[str] = "aws/sample_04"

logs: list = []
sequence: int = 0


def main() -> None:
    global logs, sequence  # Redeclare global variables

    try:
        logs.append({"message": f"[{(sequence := sequence + 1)}] === main Start ==="})

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#client
        logs.append({"message": f"[{(sequence := sequence + 1)}] S3へ接続"})
        s3 = boto3.client("s3", region_name="ap-northeast-1")

        bucket_name = f"python-test-{datetime.now().strftime('%Y%m%d')}"
        logs.append({"message": f"[{(sequence := sequence + 1)}] display bucket_name", "bucket_name": bucket_name})

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_objects_v2
        logs.append({"message": f"[{(sequence := sequence + 1)}] ファイル一覧を取得"})
        response = s3.list_objects_v2(Bucket=bucket_name)
        if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
            raise Exception("ファイル一覧取得失敗")

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_object
        for file in response["Contents"]:
            logs.append({"message": f"[{(sequence := sequence + 1)}] ファイルを取得", "key": file["Key"]})
            data = s3.get_object(Bucket=bucket_name, Key=file["Key"])
            if data["ResponseMetadata"]["HTTPStatusCode"] != 200:
                raise Exception("ファイル取得失敗")

            body_contents = data["Body"].read()
            logs.append(
                {"message": f"[{(sequence := sequence + 1)}] display body_contents", "body_contents": body_contents}
            )
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
