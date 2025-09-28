from typing import Any, Dict


class MoySkladClient:
    def __init__(self, base_url: str, token: str) -> None:
        self.base_url = base_url
        self.token = token

    async def get_status(self) -> Dict[str, Any]:
        return {"ok": True}


