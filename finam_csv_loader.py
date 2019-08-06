from yarl import URL


async def download_csv(ua, _id, _ticker, date, _tf=3, _datf=5):

    _url = URL("http://export.finam.ru/{t}_{d:%d%m%y}_{d:%d%m%y}.csv".format(t=_ticker.upper(), d=date))
    _url = _url.update_query({ 'market': 1,                     # moex акции
                               'em': _id,                       # номер инструмента
                               'apply': 0,
                               'p': _tf,                        # таймфрейм: 1 - тики, 2 - минуты; 3 - 5мин., 4 - 10мин., 7 - час, 8 - день, 9 - неделя, 10 - месяц
                               'datf': _datf,                   # csv fields collection: 12 - verbose, 5 - simple
                               'at': 1,                         # заголовки
                               'code': _ticker, 'cn': _ticker,  # тикер инструмента
                               'dtf': 3,                        # csv date format
                               'tmf': 3,                        # csv time format
                               'MSOR': 1,                       # 0 - start, 1 - end of candle
                               'df': date.day, 'dt': date.day,
                               'mf': date.month-1, 'mt': date.month-1,
                               'yf': date.year, 'yt': date.year,
                               'from': f"{date:%d.%m.%Y}", 'to': f"{date:%d.%m.%Y}",
                               'f': f"{_ticker}_{date:%d%m%y}_{date:%d%m%y}",
                               'e': '.csv',
                               'sep': 3,                        # разделитель полей
                               'sep2': 1,                       # разделитель разрядов
                               'mstime': 'on', 'mstimever': 1, })

    res = await ua.get(_url,
                       headers={ 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
                                 'Accept': '*/*',
                                 'Accept-Encoding': 'gzip, deflate',
                                 'Connection': 'close', })

    res.raise_for_status()
    # res.content is an async_generator
    _csv = await res.text()
    assert res.closed
    return _csv


async def download_5min_simple(ua, _id, _ticker, date):
    """<DATE>;<TIME>;<OPEN>;<HIGH>;<LOW>;<CLOSE>;<VOL>"""
    return await download_csv(ua, _id, _ticker, date, _tf=3, _datf=5)

async def download_tick_verbose(ua, _id, _ticker, date):
    """<DATE>;<TIME>;<LAST>;<VOL>;<ID>;<OPER>"""
    return await download_csv(ua, _id, _ticker, date, _tf=1, _datf=12)
