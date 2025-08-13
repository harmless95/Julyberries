from fastapi_users.authentication import BearerTransport

from core.config import setting

bearer_transport = BearerTransport(tokenUrl=setting.api.bearer_token_url)
