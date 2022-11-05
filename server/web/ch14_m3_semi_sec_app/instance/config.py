"""Flask configuration."""
import os

def getEnv(env, fallback=None):
    if env in os.environ:
        return os.environ.get(env)
    elif fallback:
        return fallback
    else:
        # Forced fail, to prevent unintended leak secret/solution
        raise Exception("Missing env: %s" % env)

FLASK_DEBUG = getEnv("FLASK_DEBUG", "FALSE") # FALSE/TRUE
SECRET_KEY = getEnv("SECRET_KEY")
ADMIN_PASSWORD = getEnv("ADMIN_PASSWORD")
CTF_FLAG = getEnv("CTF_FLAG")
CAPTCHA_SITE_KEY = getEnv("CAPTCHA_SITE_KEY")
CAPTCHA_SECRET_KEY = getEnv("CAPTCHA_SECRET_KEY")
