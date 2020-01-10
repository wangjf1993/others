import requests
import urllib.request
import time
import json
import os
import re
from flask import Flask, jsonify
from flask_cors import *
from functools import wraps
from flask import make_response
from lxml import etree
from flask_cors import cross_origin
import redis
import random

app = Flask(__name__)
# 跨域
CORS(app, supports_credentials=True)
from urllib import parse
from flask import request
from fake_useragent import UserAgent
from lxml import etree


# 解决跨域问题
def allow_cross_domain(fun):
    '''
    跨域装饰器
    :param fun:
    :return:
    '''

    @wraps(fun)
    def wrapper_fun(*args, **kwargs):
        rst = make_response(fun(*args, **kwargs))
        # response = make_response(jsonify(response=get_articles(ARTICLES_NAME)))

        rst.headers['Access-Control-Allow-Origin'] = '*'

        # rst.headers['Access-Control-Allow-Methods'] = 'POST,GET'
        #
        # rst.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
        # # rst.headers['Access-Control-Allow-Origin'] = '*'
        # # rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
        # allow_headers = "Referer,Accept,Origin,User-Agent"
        # rst.headers['Access-Control-Allow-Headers'] = allow_headers
        # response = make_response(jsonify(result_text))

        return rst

    return wrapper_fun


def get_random_proxy():
    """
    代理
    :return:
    """
    # response = requests.get(
    #     # 蘑菇
    #    # 'http://piping.mogumiao.com/proxy/api/get_ip_al?appKey=498e378166634e7b98bb6e1b37ede6a4&count=1&expiryDate=0&format=2&newLine=2'
    #    # 'http://piping.mogumiao.com/proxy/api/get_ip_al?appKey=cc6c3f97e4844ab3bccfe87975968278&count=1&expiryDate=0&format=2&newLine=2'
    #    'http://piping.mogumiao.com/proxy/api/get_ip_al?appKey=cc6c3f97e4844ab3bccfe87975968278&count=1&expiryDate=0&format=2&newLine=2'
    #    # 'http://tpv.daxiangdaili.com/ip/?tid=557110549118915&num=100&operator=1&delay=1'
    #     # 芝麻
    #     # 'http://webapi.http.zhimacangku.com/getip?num=1&type=1&pro=&city=0&yys=0&port=11&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions='
    #
    # )
    # proxies_values = response.text.strip()
    #
    # print(proxies_values)

    """
    代理
    :return:
    """
    redis_cli_ip = redis.Redis(host='222.212.90.13', db=7, password='Gouuse@spider',port=6579)
    while True:
        try:
            proxies_values = redis_cli_ip.lpop('proxy2').decode()
            break
        except Exception as proex:
            print(proex)
            time.sleep(random.random())
    # proxies_values = 'https://' + proxies_values
    # print('new IP: {}'.format(proxies_values))
    return proxies_values



proxies = ''

def get_yandex_urlibCookie():
    # 请求头设置
    headers = {

        'Host': 'passport.yandex.com',
        'Connection': 'close',
        'Content-Length': '46',
        'Cache-Control': 'max-age=0',
        'Origin': 'https://passport.yandex.com',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://passport.yandex.com/auth',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }

    data2 = {
        'login': '15606738584',
        'passwd': 'lijun7870305',
        'retpath': ''
    }
    data3 = {
        'login': '15984906241',
        'passwd': 'lijun7870305',
        'retpath': ''
    }
    data_list=[data2,data3]
    import random
    data=random.choice(data_list)
    url = 'https://passport.yandex.com/auth'
    from urllib import request

    from http.cookiejar import CookieJar
    import urllib.parse
    cookie = CookieJar()
    # 携带cookie值
    headler = request.HTTPCookieProcessor(cookie)
    # 处理SSL
    my_ssl = request.HTTPBasicAuthHandler
    global proxies
    proxies = get_random_proxy()

    proxies_1 = {
        'https': 'https://' + proxies}
    proxies = {
        'http': 'http://' + proxies,
        'https': 'https://' + proxies}
    proxy=urllib.request.ProxyHandler(proxies_1)

    # 构建opner
    opener = request.build_opener(headler, my_ssl,proxy)
    # 构造请求头
    req = request.Request(url=url, headers=headers, data=urllib.parse.urlencode(data).encode('utf-8'), method='POST')
    # 打开页面
    while True:
        try:
            opener.open(req)
            break
        except Exception as e:
            time.sleep(1.5)
            proxies = get_random_proxy()

            proxies_1 = {
                'https': 'https://' + proxies}
            proxies = {
                'http': 'http://' + proxies,
                'https': 'https://' + proxies}
            proxy = urllib.request.ProxyHandler(proxies_1)

            # 构建opner
            opener = request.build_opener(headler, my_ssl, proxy)
            # 构造请求头
            req = request.Request(url=url, headers=headers, data=urllib.parse.urlencode(data).encode('utf-8'),
                                  method='POST')
            print(e)
    write_cookie = {}
    for c in cookie:
        write_cookie[c.name] = c.value
    cookie = json.dumps(write_cookie)
    with open('cookie.json', 'w') as f:
        f.write(cookie)
    return write_cookie,

value = get_random_proxy()

proxies = {
    'http': 'http://' + value,
    'https': 'https://' + value}

# pc
@app.route('/', methods=['GET'])
@allow_cross_domain
def hello_world():
    '''
    返回 google ,bing,yandex,yahoo 搜索引擎 搜索结果
    :return: 状态吗 200 成功 和搜索结果页面
       '''
    mytype = request.args.get('type')
    key = request.args.get('key')
    page = request.args.get('page')
    data = {}

    if mytype == 'google':
        page = (int(page) - 1) * 10
        key = parse.quote(key)

        html = requests.get('https://www.google.com.hk/search?q={}&start={}'.format(key, page)).text
        # 解决图片显示
        html = html.replace('src="/', 'src="https://www.google.com.hk/')
        # 解决显示 和隐藏部分元素

        html = html.replace('id=gbar', 'id=gbar style="display:none"')
        # html=html.replace('id="sform"','id="sform" display:none')
        html = html.replace("border-bottom:1px ", 'border-bottom:0px ')
        html = html.replace('id=guser', ' id=guser style="display:none"')
        html = html.replace('class="sfbgg"', 'class="sfbgg" style="display:none"')
        html = html.replace('class="tn"', 'class="tn" style="display:none;border: none;"')
        html = html.replace('id="tbd"', 'id="tbd"  style="display:none"')
        html = html.replace('id="foot"', 'id="foot" style="display:none" ')
        html = html.replace('id="rhs_block"', 'id="rhs_block" style="display:none"')
        html = html.replace('href="/', 'target="_blank" href="https://www.google.com.hk/')
        html = html.replace('</head>',
                            '<script src="https://apps.bdimg.com/libs/jquery/2.1.4/jquery.min.js"></script></head>')

        # 解决跳转

        html = html.replace('style="clear:both;margin-bottom:17px;overflow:hidden"', 'style="display:none" ')

        html = html.replace("</head>",
                            "<style>#mn{width: auto !important;max-width: 640px !important;} #leftnav{display:none !important;}</style></head>")

        #  js
        js = """
           <script>

      jQuery(document).on("click","a:not(#reloadTarget)",function(event){
      event.preventDefault();
      var url = jQuery(this).attr("href");
       var newWindow = window.open(url);
      jQuery.ajax({
        url:"https://search.api.gouuse.cn/info",
        type:"get",
        data:{url:url,type:"google"},
        dataType:"json",
        success:function(res){
         if(res.code==0){
          newWindow.location.href = res.data;

         }
                }
              })
              return true;
         })
                    </script>
        """
        html = html.replace("</head>", js + '</head>')

        data['code'] = 0
        data['html'] = html
        return jsonify(data)



    elif mytype == 'bing':

        headers = {

            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        key = parse.quote(key)
        page = (int(page) - 1) * 14

        s = """
        <script type="text/javascript" >
        (function(){
          setTimeout(function(){
            var imgs = document.getElementsByTagName('img');
            for(var i = 0; i < imgs.length; i++){
              var src = imgs[i].getAttribute("data-src-hq")
              src&&imgs[i].setAttribute("src","https://www.bing.com"+src);
            }
          },1000)
        })()
        </script>
        </body>
        """
        # try:
        for _ in range(3):
            try:
                req = urllib.request.Request('https://www.bing.com/search?q={}&first={}'.format(key, page),
                                             headers=headers)
                rep = urllib.request.urlopen(req, timeout=30)
                break
            except urllib.error.URLError:
                print('链接超时')
        html = rep.read().decode('utf-8')

        # 解决图片
        content = etree.HTML(html)
        imgs = content.xpath('//img')
        for img in imgs:
            t = img.xpath('@src')
            if len(t) > 0:
                html = html.replace('data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAEALAAAAAABAAEAAAIBTAA7',
                                    'https://cn.bing.com' + t[0])
        # 解决显示 和隐藏部分元素
        html = html.replace('id="b_header"', 'id="b_header" style="display:none"')
        html = html.replace('class="b_msg"', 'class="b_msg" style="display:none"')
        html = html.replace('role="complementary"', 'role="complementary" style="display:none"')
        html = html.replace('hover-trans="no"', 'hover-trans="no" style="display:none"')
        html = html.replace('class="b_pag"', 'class="b_pag" style="display:none"')
        html = html.replace('id="b_footer"', 'id="b_footer" style="display:none"')
        html = html.replace('<a', '<a target="_blank"')
        html = html.replace('class="b_rs"', 'class="b_rs" style="display:none"')
        html = html.replace('</body>', s)
        html = html.replace("</head>",
                            "<style>body{min-width:640px !important;} #b_content{padding: 10px !important;}</style></head>")

        data['code'] = 0
        data['html'] = html
        return jsonify(data)


    elif mytype == 'yahoo':
        headers = {

            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }

        page = (int(page) - 1) * 10 + 1
        try:
            for _ in range(3):
                try:
                    html = requests.get(url='https://search.yahoo.com/search?p={}&b={}'.format(key, page),
                                        headers=headers, verify=False).text
                    break
                except:
                    print('链接超时')

            # 解决显示 和隐藏部分元素
            html = html.replace('id="sticky-hd"', 'id="sticky-hd" style="display:none"')
            html = html.replace('id="horizontal-bar"', 'id="horizontal-bar" style="display:none"')
            html = html.replace('id="right"', 'id="right" style="display:none"')
            html = html.replace('id="sticky-hd"', 'd="sticky-hd" style="display:none"')
            html = html.replace('id="horizontal-bar"', 'id="horizontal-bar" style="display:none"')
            html = html.replace('id="right"', 'id="right" style="display:none"')
            html = html.replace('class="compPagination"', 'class="compPagination" style="display:none"')
            html = html.replace('id="ft_wrapper"', 'id="ft_wrapper" style="display:none"')
            html = html.replace('class="dd AlsoTry"', 'class="dd AlsoTry" style="display:none" ')
            html = html.replace("</head>",
                                "<style>#bd{min-width:640px !important} #bd #results{padding-left:0px !important;}</style></head>")
            html = html.replace('</head>',
                                '<script src="https://apps.bdimg.com/libs/jquery/2.1.4/jquery.min.js"></script></head>')
            #  js
            js = """
                      <script>

                 jQuery(document).on("click","a:not(#reloadTarget)",function(event){
                 event.preventDefault();
                 var url = jQuery(this).attr("href");
                  var newWindow = window.open(url);
                 jQuery.ajax({
                   url:"https://search.api.gouuse.cn/info",
                   type:"get",
                   data:{url:url,type:"yahoo"},
                   dataType:"json",
                   success:function(res){
                    if(res.code==0){
                     newWindow.location.href = res.data;

                    }
                   }
                 })
                 return true;
            })
                       </script>
                   """
            html = html.replace("</head>", js + '</head>')
        except:
            html = None

        data['code'] = 0
        data['html'] = html
        return jsonify(data)
    elif mytype == 'yandex':
        headers = {

            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'www.yandex.com',
            'Referer': 'https://www.yandex.com/',
            'Upgrade-Insecure-Requests': '1',
            # 'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.0; en-us; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
            'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Mobile Safari/537.36'

        }
        cookies = ''
        with open('cookie.json', 'r', encoding='utf-8') as f:
            cookies = f.read()
        cookies = json.loads(cookies)
        url = 'https://www.yandex.com/search/touch/?text={}&p={}'.format(key, page)
        while  True:
            try:
                global proxies
                value = get_random_proxy()
                proxies = {
                    'http': 'http://' + value,
                    'https': 'https://' + value}
                html = requests.get(url, headers=headers, cookies=cookies, verify=False, proxies=proxies).text
                break
            except Exception as e:

                print(e)
                # cookies = get_yandex_urlibCookie()
                pass
        print(html)
        content = etree.HTML(html)

        title = content.xpath('/html/head/title/text()')[0]
        if title == 'Oops!':
            for _ in range(10):
                # cookies = get_yandex_urlibCookie()
                print('换ip')
                value = get_random_proxy()

                proxies = {
                    'http': 'http://' + value,
                    'https': 'https://' + value}
                try:
                    html = requests.get(url, headers=headers, timeout=20, cookies=cookies, proxies=proxies).text
                    content = etree.HTML(html)
                except:

                    time.sleep(1)
                title = content.xpath('/html/head/title/text()')[0]
                if title != 'Oops!':
                    break
        html = html.replace('class="header3 i-bem" ', 'class="header3 i-bem" style="display:none" ')
        html = html.replace('class=region-change', 'class=region-change style="display:none"')
        html = html.replace('class="button2 button2_size_m button2_theme_default button2_view_classic i-bem"',
                            'class="button2 button2_size_m button2_theme_default button2_view_classic i-bem" style="display:none" ')
        html = html.replace('serp-footer__grid grid grid_pad-x_yes grid_centered_yes"',
                            'serp-footer__grid grid grid_pad-x_yes grid_centered_yes" style="display:none" ')
        html = html.replace('class="serp-footer flex-none serp i-bem"',
                            'style="display:none" class="serp-footer flex-none serp i-bem" ')
        html = html.replace('class=pager', 'class=pager style="display:none"  ')
        html = html.replace('class="yandex-search grid"', 'class="yandex-search grid" style="display:none" ')
        html = html.replace('class=footer2 ', 'class=footer2  style="display:none" ')
        html = html.replace('class=competitors', 'class=competitors style="display:none"')
        html = html.replace('class=footer', 'class=footer  style="display:none"')
        html = html.replace('class=serp-header__main', 'class=serp-header__main style="display:none"')
        html = html.replace('class="serp-navigation z-index-group z-index-group_level_8"',
                            'class="serp-navigation z-index-group z-index-group_level_8" style="display:none"')
        html = html.replace('class="serp-list serp-list_right_yes"',
                            'class="serp-list serp-list_right_yes"  style="display:none"')
        html = html.replace('class=serp-adv__found', 'class=serp-adv__found style="display:none"')
        html = html.replace('role=contentinfo', 'role=contentinfo  style="display:none"')
        html = html.replace('class="pager i-bem"', 'class="pager i-bem" style="display:none"')
        html = html.replace('class=competitors', 'class=competitors style="display:none"')
        html = html.replace("""data-bem='{"link":{}}'""", """ """)
        html = html.replace("</body>", "<style> body:{background:#fff;}  body > .grid{margin: 0;}</style></body>")
        data['code'] = 0
        data['html'] = html
        return jsonify(data)

    else:
        return jsonify({'code': 400, 'html': '请求错误'})


# 跳转详情页
@app.route('/info', methods=['GET'])
@allow_cross_domain
def info():
    mytype = request.args.get('type')
    url = request.args.get('url')
    if mytype == 'google':
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }
        t = requests.get(url=url, headers=headers, verify=False)
        url = t.request.url
        url = url.replace('https://www.google.com.hk/url?q=', '')
        data = {'code': 0, 'data': url}
        return jsonify(data)
    if mytype == "yahoo":
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }
        t = requests.get(url=url, headers=headers, verify=False)
        html = etree.HTML(t.text)
        t = html.xpath('//meta[@http-equiv="refresh"]/@content')
        t = t[0].replace('0;URL=', '')
        t = t.replace("'", '')
        data = {'code': 0, 'data': t}
        return jsonify(data)


# app
@app.route('/app', methods=['GET'])
@allow_cross_domain
def apphtml():
    mytype = request.args.get('type')
    key = request.args.get('key')
    page = request.args.get('page')
    data = {}

    if mytype == 'google':
        page = (int(page) - 1) * 10
        key = parse.quote(key)
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
        }

        html = requests.get('https://www.google.com.hk/search?q={}&start={}'.format(key, page), headers=headers).text
        html = html.replace('class="card"', 'class="card" style="display:none"')
        html = html.replace('id="botstuff"', 'id="botstuff" style="display:none"')
        html = html.replace('id="qslc"', 'id="qslc" style="display:none" ')
        html = html.replace('id="sfooter"', 'id="sfooter" style="display:none"  ')
        html = html.replace('id="navd"', 'id="navd" style="display:none" ')
        html = html.replace('id="sfcnt"', 'id="sfcnt" style="display:none" ')
        html = html.replace('id="hdtb-sc"', 'id="hdtb-sc" style="display:none" ')
        html = html.replace('class="card TshKde"', 'class="card TshKde" style="display:none" ')
        html = html.replace('id="msc"', 'id="msc" style="display:none"  ')
        data['code'] = 0
        data['data'] = html
        return jsonify(data)
        # return html
    elif mytype == 'bing':
        page = (int(page) - 1) * 10
        key = parse.quote(key)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.0; en-us; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
        }
        # key = parse.quote(key)
        page = (int(page) - 1) * 14
        html = requests.get(
            'https://cn.bing.com/search?q={}&qs=HS&pq=kao&sc=8-3&sp=1&first={}&FORM=PERE1'.format(key, page),
            headers=headers).text
        html = html.replace('id="b_header"', 'id="b_header" style="display:none"')
        html = html.replace('<a', '<a target="_blank"')
        html = html.replace('id="b_header"', 'id="b_header" style="display:none"')
        html = html.replace('class="b_pag"', 'class="b_pag" style="display:none"')
        html = html.replace('id="b_footer"', 'id="b_footer" style="display:none"')
        html = html.replace('class="b_ans"', 'class="b_ans" style="display:none"')
        html = html.replace('class="b_msg"', 'class="b_msg" style="display:none"')
        html = html.replace('id="results_removed"', 'id="results_removed" style="display:none"')
        data['code'] = 0
        data['data'] = html
        return jsonify(data)
    elif mytype == 'yahoo':

        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
        }

        page = (int(page) - 1) * 10 + 1

        for _ in range(3):
            try:
                html = requests.get(url='https://search.yahoo.com/search?p={}&b={}'.format(key, page),
                                    headers=headers, verify=False).text
                break
            except:
                print('链接超时')
        html = html.replace('id="header"', 'id="header" style="display:none"')
        html = html.replace('id="pivot"', 'id="pivot"style="display:none" ')
        html = html.replace('class="reg searchCenterFooter"', 'class="reg searchCenterFooter" style="display:none" ')
        html = html.replace('class="reg searchBottom"', 'class="reg searchBottom" style="display:none"')
        html = html.replace('id="footer"', 'id="footer" style="display:none"')
        html = html.replace('<a', '<a target="_blank"')
        data['code'] = 0
        data['data'] = html
        return jsonify(data)
    elif mytype == 'yandex':
        headers = {

            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'www.yandex.com',
            'Referer': 'https://www.yandex.com/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.0; en-us; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'

        }
        cookies = ''
        with open('cookie.json', 'r', encoding='utf-8') as f:
            cookies = f.read()
        cookies = json.loads(cookies)
        url = 'https://www.yandex.com/search/touch/?text={}&p={}'.format(key, page)
        while True:
            try:
                global proxies
                value = get_random_proxy()

                proxies = {
                    'http': 'http://' + value,
                    'https': 'https://' + value}
                html = requests.get(url, headers=headers, cookies=cookies, verify=False, proxies=proxies).text
                break
            except Exception as e:
                print(e)


        content = etree.HTML(html)
        title = content.xpath('/html/head/title/text()')[0]
        if title == 'Oops!':
            for _ in range(10):
                cookies = get_yandex_urlibCookie()
                print('换ip')
                # value = get_random_proxy()

                try:

                    value = get_random_proxy()

                    proxies = {
                        'http': 'http://' + value,
                        'https': 'https://' + value}
                    html = requests.get(url, headers=headers, timeout=20, cookies=cookies, proxies=proxies).text
                    content = etree.HTML(html)
                except:
                    pass
                    # value = get_random_proxy()
                    #
                    # proxies = {
                    #     'http': 'http://' + value,
                    #     'https': 'https://' + value}
                title = content.xpath('/html/head/title/text()')[0]
                if title != 'Oops!':
                    break
        html = html.replace('class="header3 i-bem" ', 'class="header3 i-bem" style="display:none" ')
        html = html.replace('class=region-change', 'class=region-change style="display:none"')
        html = html.replace('class="button2 button2_size_m button2_theme_default button2_view_classic i-bem"',
                            'class="button2 button2_size_m button2_theme_default button2_view_classic i-bem" style="display:none" ')
        html = html.replace('serp-footer__grid grid grid_pad-x_yes grid_centered_yes"',
                            'serp-footer__grid grid grid_pad-x_yes grid_centered_yes" style="display:none" ')
        html = html.replace('class="serp-footer flex-none serp i-bem"',
                            'style="display:none" class="serp-footer flex-none serp i-bem" ')
        html = html.replace('class=pager', 'class=pager style="display:none"  ')
        html = html.replace('class="yandex-search grid"', 'class="yandex-search grid" style="display:none" ')
        html = html.replace('class=footer2 ', 'class=footer2  style="display:none" ')
        html = html.replace('class=competitors', 'class=competitors style="display:none"')
        html = html.replace('class=footer', 'class=footer  style="display:none"')
        html = html.replace('class=serp-header__main', 'class=serp-header__main style="display:none"')
        html = html.replace('class="serp-navigation z-index-group z-index-group_level_8"',
                            'class="serp-navigation z-index-group z-index-group_level_8" style="display:none"')
        html = html.replace('class="serp-list serp-list_right_yes"',
                            'class="serp-list serp-list_right_yes"  style="display:none"')
        html = html.replace('class=serp-adv__found', 'class=serp-adv__found style="display:none"')
        html = html.replace('role=contentinfo', 'role=contentinfo  style="display:none"')
        html = html.replace('class="pager i-bem"', 'class="pager i-bem" style="display:none"')
        html = html.replace('class=competitors', 'class=competitors style="display:none"')
        html = html.replace("""data-bem='{"link":{}}'""", """ """)

        data['code'] = 0
        data['data'] = html
        return jsonify(data)

    else:
        data['code'] = 400
        data['data'] = '请正确传参'
        return jsonify(data)


# test
@app.route('/test', methods=['GET'])
@allow_cross_domain
def testhtml():
    mytype = request.args.get('type')
    key = request.args.get('key')
    page = request.args.get('page')
    data = {}

    if mytype == 'google':
        page = (int(page) - 1) * 10
        key = parse.quote(key)
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
        }

        html = requests.get('https://www.google.com.hk/search?q={}&start={}'.format(key, page), headers=headers).text
        html = html.replace('class="card"', 'class="card" style="display:none"')
        html = html.replace('id="botstuff"', 'id="botstuff" style="display:none"')
        html = html.replace('id="qslc"', 'id="qslc" style="display:none" ')
        html = html.replace('id="sfooter"', 'id="sfooter" style="display:none"  ')
        html = html.replace('id="navd"', 'id="navd" style="display:none" ')
        html = html.replace('id="sfcnt"', 'id="sfcnt" style="display:none" ')
        html = html.replace('id="hdtb-sc"', 'id="hdtb-sc" style="display:none" ')
        html = html.replace('class="card TshKde"', 'class="card TshKde" style="display:none" ')
        html = html.replace('id="msc"', 'id="msc" style="display:none"  ')
        data['code'] = 0
        data['data'] = html
        # return jsonify(data)
        return html
    elif mytype == 'bing':
        page = (int(page) - 1) * 10
        key = parse.quote(key)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.0; en-us; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
        }
        # key = parse.quote(key)
        page = (int(page) - 1) * 14
        html = requests.get(
            'https://cn.bing.com/search?q={}&qs=HS&pq=kao&sc=8-3&sp=1&first={}&FORM=PERE1'.format(key, page),
            headers=headers).text
        html = html.replace('id="b_header"', 'id="b_header" style="display:none"')
        html = html.replace('<a', '<a target="_blank"')
        html = html.replace('id="b_header"', 'id="b_header" style="display:none"')
        html = html.replace('class="b_pag"', 'class="b_pag" style="display:none"')
        html = html.replace('id="b_footer"', 'id="b_footer" style="display:none"')
        html = html.replace('class="b_ans"', 'class="b_ans" style="display:none"')
        html = html.replace('class="b_msg"', 'class="b_msg" style="display:none"')
        html = html.replace('id="results_removed"', 'id="results_removed" style="display:none"')
        data['code'] = 0
        data['data'] = html
        # return jsonify(data)
        return html
    elif mytype == 'yahoo':

        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
        }

        page = (int(page) - 1) * 10 + 1

        for _ in range(3):
            try:
                html = requests.get(url='https://search.yahoo.com/search?p={}&b={}'.format(key, page),
                                    headers=headers, verify=False).text
                break
            except:
                print('链接超时')
        html = html.replace('id="header"', 'id="header" style="display:none"')
        html = html.replace('id="pivot"', 'id="pivot"style="display:none" ')
        html = html.replace('class="reg searchCenterFooter"', 'class="reg searchCenterFooter" style="display:none" ')
        html = html.replace('class="reg searchBottom"', 'class="reg searchBottom" style="display:none"')
        html = html.replace('id="footer"', 'id="footer" style="display:none"')
        html = html.replace('<a', '<a target="_blank"')
        data['code'] = 0
        data['data'] = html
        # return jsonify(data)
        return html
    elif mytype == 'yandex':
        headers = {

            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'www.yandex.com',
            'Referer': 'https://www.yandex.com/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.0; en-us; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'

        }
        cookies = ''
        with open('cookie.json', 'r', encoding='utf-8') as f:
            cookies = f.read()
        cookies = json.loads(cookies)

        url = 'https://www.yandex.com/search/touch/?text={}&p={}'.format(key, page)
        while True:
            try:
                html = requests.get(url, headers=headers, cookies=cookies, verify=False, proxies=proxies).text
                break
            except:
                value = get_random_proxy()
                proxies = {
                    'http': 'http://' + value,
                    'https': 'https://' + value}
        content = etree.HTML(html)
        title = content.xpath('/html/head/title/text()')[0]
        if title == 'Oops!':
            for _ in range(10):
                cookies = get_yandex_urlibCookie()
                print('换ip')
                value = get_random_proxy()
                proxies = {
                    'http': 'http://' + value,
                    'https': 'https://' + value}
                try:
                    html = requests.get(url, headers=headers, timeout=20, cookies=cookies, proxies=proxies).text
                    content = etree.HTML(html)
                except:
                    time.sleep(1)
                title = content.xpath('/html/head/title/text()')[0]
                if title != 'Oops!':
                    break
        html = html.replace('class="header3 i-bem" ', 'class="header3 i-bem" style="display:none" ')
        html = html.replace('class=region-change', 'class=region-change style="display:none"')
        html = html.replace('class="button2 button2_size_m button2_theme_default button2_view_classic i-bem"',
                            'class="button2 button2_size_m button2_theme_default button2_view_classic i-bem" style="display:none" ')
        html = html.replace('serp-footer__grid grid grid_pad-x_yes grid_centered_yes"',
                            'serp-footer__grid grid grid_pad-x_yes grid_centered_yes" style="display:none" ')
        html = html.replace('class="serp-footer flex-none serp i-bem"',
                            'style="display:none" class="serp-footer flex-none serp i-bem" ')
        html = html.replace('class=pager', 'class=pager style="display:none"  ')
        html = html.replace('class="yandex-search grid"', 'class="yandex-search grid" style="display:none" ')
        html = html.replace('class=footer2 ', 'class=footer2  style="display:none" ')
        html = html.replace('class=competitors', 'class=competitors style="display:none"')
        html = html.replace('class=footer', 'class=footer  style="display:none"')
        html = html.replace('class=serp-header__main', 'class=serp-header__main style="display:none"')
        html = html.replace('class="serp-navigation z-index-group z-index-group_level_8"',
                            'class="serp-navigation z-index-group z-index-group_level_8" style="display:none"')
        html = html.replace('class="serp-list serp-list_right_yes"',
                            'class="serp-list serp-list_right_yes"  style="display:none"')
        html = html.replace('class=serp-adv__found', 'class=serp-adv__found style="display:none"')
        html = html.replace('role=contentinfo', 'role=contentinfo  style="display:none"')
        html = html.replace('class="pager i-bem"', 'class="pager i-bem" style="display:none"')
        html = html.replace('class=competitors', 'class=competitors style="display:none"')
        html = html.replace("""data-bem='{"link":{}}'""", """ """)
        html = html.replace("</body>",'<style> body:{background:#fff;}  body > .grid.grid{margin: 0;}</style>')

        data['code'] = 0
        data['data'] = html
        return jsonify(data)

    else:
        data['code'] = 400
        data['data'] = '请正确传参'
        return jsonify(data)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
    # app.run(debug=True)
