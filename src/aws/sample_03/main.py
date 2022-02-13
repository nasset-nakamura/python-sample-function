import traceback
from datetime import datetime
from pprint import pprint
from typing import Final

import boto3

FUNCTION_NAME: Final[str] = "aws/sample_03"

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

        files: list[dict] = [
            {
                "Key": "test/test_01.csv",
                "Body": b'"col1","col2","col3"\n"aaa","bbb","ccc"\n"ddd","eee","fff"',
            },
            {"Key": "test/test_02.json", "Body": str(logs)},
        ]

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_object
        # https://dev.classmethod.jp/articles/boto3-s3-object-put-get/
        # https://tasotasoso.hatenablog.com/entry/2019/01/13/171819
        for file in files:
            logs.append({"message": f"[{(sequence := sequence + 1)}] ファイルを追加", "key": file["Key"]})
            response = s3.put_object(
                Bucket=bucket_name,
                Key=file["Key"],
                Body=file["Body"],
            )
            if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
                raise Exception("ファイル追加失敗")
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
