from typing import Any, Dict


class GoogleSheetsClient:
    def __init__(self, token: str) -> None:
        self.token = token

    async def get_status(self) -> Dict[str, Any]:
        return {"ok": True}


