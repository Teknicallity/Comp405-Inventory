import sys

config = None
if 'pytest' in sys.argv or 'unittest' in sys.argv:
    from .test import TestConfig
    config = TestConfig()
else:
    try:
        from .dev import DevConfig
        config = DevConfig()
    except ImportError:
        from .prod import ProdConfig
        config = ProdConfig()
