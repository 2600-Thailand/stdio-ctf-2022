"""Flask configuration."""
import os

def getEnv(env, fallback):
    if env in os.environ:
        return os.environ.get(env)
    else:
        return fallback

FLASK_ENV = getEnv("FLASK_ENV", "production") # or development
SECRET_KEY = getEnv("SECRET_KEY", "HelloWorld")
ADMIN_PASSWORD = getEnv("ADMIN_PASSWORD", "HelloWorld")
CTF_FLAG = getEnv("CTF_FLAG", "FLAG{NOT_THIS_ONE_BRUH}")
CAPTCHA_SITE_KEY = getEnv("CAPTCHA_SITE_KEY", "")
CAPTCHA_SECRET_KEY = getEnv("CAPTCHA_SECRET_KEY", "")
