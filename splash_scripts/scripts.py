from scrapy_splash import SplashRequest

with open("splash_scripts/default.lua", "r") as default:
    default_script = default.read()

with open("splash_scripts/scroll_down.lua", "r") as scroll_down:
    scroll_down_script = scroll_down.read()    