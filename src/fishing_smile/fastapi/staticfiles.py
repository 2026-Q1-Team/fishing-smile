from starlette.responses import Response
from starlette.types import Scope

from starlette.staticfiles import StaticFiles


class CacheControlledStaticFiles(StaticFiles):

    def __init__(
        self, *args,
        cache_control: str | None = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.cache_control = cache_control

    async def get_response(self, path: str, scope: Scope) -> Response:
        response = await super().get_response(path, scope)
        if self.cache_control:
            response.headers['Cache-Control'] = self.cache_control
        return response
