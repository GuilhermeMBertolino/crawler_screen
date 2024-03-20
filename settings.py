BOT_NAME = "firmwares"
SPIDER_MODULES = ["spiders"]
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(levelname)s: %(message)s"
HTTPERROR_ALLOWED_CODES = [404]

SPLASH_URL = 'http://192.168.150.3:8050'
DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}
SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'