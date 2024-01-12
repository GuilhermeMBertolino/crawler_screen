function main(splash, args)
    local scroll_delay = 2
    local max_scrolls = 50
    local scroll_count = 0

    while scroll_count < max_scrolls do
        splash:wait(scroll_delay)
        splash:runjs("window.scrollTo(0, document.body.scrollHeight);")
        scroll_count = scroll_count + 1
    end

    splash:wait(scroll_delay)
    return splash:html()
end