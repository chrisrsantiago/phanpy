"""FormEncode Validators."""
from openid.yadis.discover import discover
from formencode.validators import String

__all__ = ['OpenId']


class OpenId(String):
    """Verify that the provided URI/XRI is an OpenID."""
    def _to_python(self, value, c):
        try:
            discovery = discover(value)
        except:
            raise Invalid('Invalid OpenID', value, c)
        return String._to_python(self, value, c)