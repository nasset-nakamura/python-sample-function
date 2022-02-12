import traceback
from pprint import pprint
from typing import Final

from pydantic import BaseSettings
from sendgrid.helpers.mail import Mail

from sendgrid import SendGridAPIClient

FUNCTION_NAME: Final[str] = "sendgrid/sample_02"

logs: list = []
sequence: int = 0


class Config(BaseSettings):
    sendgrid_api_key: str
    sendgrid_to: str
    sendgrid_from: str
    sendgrid_template_id: str

    class Config:
        env_file = ".env"


def main() -> None:
    global logs, sequence  # Redeclare global variables

    try:
        logs.append({"message": f"[{(sequence := sequence + 1)}] === main Start ==="})
        config = Config()

        logs.append({"message": f"[{(sequence := sequence + 1)}] SendGrid APIキーを設定"})
        sendGrid = SendGridAPIClient(config.sendgrid_api_key)

        mail = Mail(
            from_email=config.sendgrid_from,
            to_emails=config.sendgrid_to,
        )
        mail.template_id = config.sendgrid_template_id
        mail.dynamic_template_data = {
            "title": "Pythonからの送信テスト!!",
            "name": "test test test",
        }

        # https://github.com/sendgrid/sendgrid-python
        # https://github.com/sendgrid/sendgrid-python/blob/main/use_cases/README.md
        # <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: ... エラーが発生する場合
        # https://hitoribucho.com/post/20190328193204
        logs.append({"message": f"[{(sequence := sequence + 1)}] HTMLメールを送信"})
        response = sendGrid.send(mail)
        if response.status_code != 202:
            raise Exception("メール送信失敗")
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
