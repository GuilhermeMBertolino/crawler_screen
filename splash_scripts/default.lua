function main(splash)
    assert(splash:go(splash.args.url))
    assert(splash:wait(splash.args.wait))
    return splash:html()
end