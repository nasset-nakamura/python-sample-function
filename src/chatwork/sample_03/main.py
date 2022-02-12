import json
import traceback
from pprint import pprint
from typing import Final

import requests
from pydantic import BaseSettings

FUNCTION_NAME: Final[str] = "chatwork/sample_03"
CHATWORK_BASE_URL: Final[str] = "https://api.chatwork.com/v2"

logs: list = []
sequence: int = 0


class Config(BaseSettings):
    chatwork_api_key: str
    chatwork_room_id: str

    class Config:
        env_file = ".env"


def main() -> None:
    global logs, sequence  # Redeclare global variables

    try:
        logs.append({"message": f"[{(sequence := sequence + 1)}] === main Start ==="})
        config = Config()

        # https://developer.chatwork.com/ja/endpoints.html
        # https://developer.chatwork.com/ja/endpoint_rooms.html#POST-rooms-room_id-messages
        logs.append({"message": f"[{(sequence := sequence + 1)}] メッセージを送信"})
        body = "aaa,bbb,ccc\nddd,eee,fff\nggg,hhh"
        response = requests.post(
            f"{CHATWORK_BASE_URL}/rooms/{config.chatwork_room_id}/messages",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "X-ChatWorkToken": config.chatwork_api_key,
            },
            params={"body": f"{body}", "self_unread": 1},
        )
        if response.status_code != 200:
            raise Exception("メッセージ送信失敗")

        # str→dict
        # pprint(json.loads(response.text))
        # # dict→str
        # pprint(json.dumps(json.loads(response.text), indent=2))

        logs.append(
            {
                "message": f"[{(sequence := sequence + 1)}] display massage_id",
                "message_id": json.loads(response.text)["message_id"],
            }
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
