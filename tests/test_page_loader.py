# -*- coding:utf-8 -*-

"""Testing all modules page-loader."""

import re
import pytest

ACTUAL_URL = 'path_to_file'

def test_get_name_from_url():

    with open(ACTUAL_URL) as url:
        actual = url.read().strip().split()

    actuals = map(get_name_from_url, actual)
    expected = re.compile(r'^[\w-]+\.html')
    
    for actual in actuals:
        assert actual == expected, "URL does not match pattern"
    
http://www.example.com/index.html
https://ru.hexlet.io/courses
https://en.wikipedia.org/wiki/URL
https://aliexpress.ru/home.htm
https://campaign.aliexpress.com/wow/gcp/ae/channel/ae/accelerate/tupr?spm=a2g0o.home.15027.1.17ba5c98ckbHwJ&wh_pid=ae/mega/ae/2020_super_friday/shoes&wh_weex=true&_immersiveMode=true&wx_navbar_hidden=true&wx_navbar_transparent=true&ignoreNavigationBar=true&wx_statusbar_hidden=true&gps-id=300000000564511&productIds=4001132140041
https://admiralmarkets.com/ru/education/articles/trading-instruments/index-sp500-trading
https://disenowebakus.net/imagenes/logo-akus.jpg
https://developer.mozilla.org/en-US/docs/Learn
https://aliexpress.ru/item/32813937749.html?spm=a2g0o.detail.1000014.8.4b7613fewRhqry&gps-id=pcDetailBottomMoreOtherSeller&scm=1007.14976.157518.0&scm_id=1007.14976.157518.0&scm-url=1007.14976.157518.0&pvid=9db37213-0a22-456a-bb4e-c15adc595ecf&_t=gps-id:pcDetailBottomMoreOtherSeller,scm-url:1007.14976.157518.0,pvid:9db37213-0a22-456a-bb4e-c15adc595ecf,tpp_buckets:668%230%23131923%2358_668%23808%236395%23442_668%23888%233325%2319_4976%230%23157518%230_4976%232711%237538%23324_4976%233223%2310815%238_4976%233104%239653%237_4976%233141%239887%231_668%232846%238111%23489_668%232717%237566%23859_&_ga=2.195680741.859224365.1594002038-431412820.1580367853
https://www.windy.com/ru/-%D0%A0%D0%9C2-5-pm2p5?cams,pm2p5,55.332,86.054,11a
