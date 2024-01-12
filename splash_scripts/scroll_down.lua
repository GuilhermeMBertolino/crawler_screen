-- function main(splash, args)
--     local scroll_delay = 0.5
--     local max_scrolls = 5
--     local scroll_count = 0

--     while scroll_count < max_scrolls do
--         splash:wait(scroll_delay)
--         splash:runjs("window.scrollTo(0, document.body.scrollHeight);")
--         scroll_count = scroll_count + 1
--     end

--     splash:wait(scroll_delay)
--     return splash:html()
-- end

function main(splash)
    local num_scrolls = 5
    local scroll_delay = 0.5

    local scroll_to = splash:jsfunc("window.scrollTo")
    local get_body_height = splash:jsfunc(
        "function() {return document.body.scrollHeight;}"
    )
    assert(splash:go(splash.args.url))
    splash:wait(splash.args.wait)

    for _ = 1, num_scrolls do
        scroll_to(0, get_body_height())
        splash:wait(scroll_delay)
    end        
    return splash:html()
end