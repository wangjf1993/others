window.__LOCALE__ = 'SG';
window.__ENV__ = 'live';
window.__TRANSIFY_MAPPING__ = {
    "id-live": "1561609277",
    "en-live": "1561609266",
    "ms-my-live": "1561609268",
    "zh-hans-live": "1561609270",
    "zh-hant-live": "1561704137",
    "th-live": "1561609274",
    "vi-live": "1561609267",
    "format": "json"
};


function showBody() {
    document && document.body && (document.body.style.visibility = "visible")
}
var SHORT_URL_MAX_LENGTH = 256,
pathname = location && location.pathname;
if ("/" !== pathname && pathname.length < SHORT_URL_MAX_LENGTH && "" === location.hash && -1 === pathname.indexOf("-") && 0 === pathname.lastIndexOf("/")) {
    document && document.body && (document.body.style.visibility = "hidden"),
    setTimeout(showBody, 5e3);
    var xhr = new XMLHttpRequest;
    xhr.open("GET", "/api/v0/is_short_url/?path=" + pathname.replace("/", "")),
    xhr.setRequestHeader("Content-Type", "application/json"),
    xhr.setRequestHeader("Accept", "application/json"),
    xhr.onreadystatechange = function() {
        if (4 === this.readyState) if (200 === this.status) if (JSON.parse(this.responseText).error) showBody();
        else {
            var e = document.createElement("a");
            e.href = location.href,
            e.search += "?" === e.search[0] ? "&__classic__=1": "?__classic__=1",
            location.href = e.href
        } else showBody()
    },
    xhr.send()
}


if (window.ga = window.ga ||
function() { (ga.q = ga.q || []).push(arguments)
},
ga.l = +new Date, window.PerformanceObserver) {
    var observer = new window.PerformanceObserver(function(e) {
        for (var r = e.getEntries(), n = 0; n < r.length; n++) {
            var a = r[n],
            i = a.name,
            t = Math.round(a.startTime + a.duration);
            ga("send", {
                hitType: "timing",
                timingCategory: "Performance Metrics",
                timingVar: i,
                timingValue: t
            })
        }
    });
    observer.observe({
        entryTypes: ["paint"]
    })
}


