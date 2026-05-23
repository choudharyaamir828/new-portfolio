from rest_framework.renderers import JSONRenderer


class APIResponseRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = None
        if renderer_context is not None:
            response = renderer_context.get("response")

        if response is not None and response.status_code >= 400:
            payload = {
                "success": False,
                "data": None,
                "errors": data,
            }
        else:
            payload = {
                "success": True,
                "data": data,
                "errors": None,
            }

        return super().render(payload, accepted_media_type, renderer_context)
