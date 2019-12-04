from django.db import models

# Create your models here.
from django.db import models

class User(models.Model):
    class Meta:
        db_table = 'user'

    userId = models.IntegerField(primary_key=True, db_column='userId')
    userName = models.CharField(max_length = 20)
    phone = models.CharField(max_length = 20, null = True)
    password = models.CharField(max_length = 64)
    email = models.CharField(max_length = 20, null = True)
    avatar = models.CharField(max_length = 100, null=True)
    signature = models.CharField(max_length = 100, null=True)
    title = models.CharField(max_length = 20, null=True)
    group = models.CharField(max_length = 50, null=True)
    notifyCount = models.IntegerField(null=True)
    unreadCount = models.IntegerField(null=True)
    country = models.CharField(max_length = 120, null=True)
    address = models.CharField(max_length = 100, null=True)
    InitialInterest = models.FloatField(null=True)  # 期初权益
    bond = models.FloatField(null=True)  # 保证金
    profitInPosition = models.FloatField(null=True)  # 持仓盈亏
    profitInClosePosition = models.FloatField(null=True)  # 平仓盈亏
    currentInterest = models.FloatField(null=True)  # 当前权益
    availableFund = models.FloatField(null=True)  # 可用资金
    profile = models.CharField(max_length = 500, null=True)
    PwdStrength = models.CharField(max_length = 10, null=True)
    registerTime = models.CharField(max_length = 30, null=True)
    def __repr__(self):
        return "".format(self.userId, self.phone)

    __str__ = __repr__


class Book(models.Model):
    class Meta:
        db_table = 'book'
    id = models.IntegerField(primary_key=True, db_column='id')
    bookName = models.CharField(max_length = 20)
    author = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    publish = models.CharField(max_length = 20, null=True)

    def __repr__(self):
        return "".format(self.bookName, self.author)

    __str__ = __repr__


class Tick_1min(models.Model):
    class Meta:
        db_table = 'tick_1min'

    TRADINGDAY = models.CharField(max_length=30, null=True) # 交易日
    INSTRUMENTID = models.CharField(max_length=20, null=True) # 合约号
    EXCHANGEID = models.CharField(max_length=10, null=True) # 交易所
    CLOSEPRICE = models.FloatField(null=True)  # 收盘价
    OPENPRICE = models.FloatField(null=True)  # 开盘价
    HIGHESTPRICE = models.FloatField(null=True)  # 最高价
    LOWESTPRICE = models.FloatField(null=True)  # 最低价
    VOLUME = models.FloatField(null=True)  # 成交量
    CHANGEAMOUT = models.FloatField(null=True)  # 涨跌
    CHANGERATE = models.FloatField(null=True)  # 涨跌幅度
    TURNOVER = models.FloatField(null=True)  # 成交金额
    OPENINTEREST = models.FloatField(null=True) # 持仓量
    SETTLEMENTPRICE = models.FloatField(null=True) # 本次结算价
    UPDATETIME = models.CharField(max_length=30, null=True) # 修改时间
    AVERAGEPRICE = models.FloatField(null=True) # 当日均价
    ACTIONDAY = models.CharField(max_length=30, null=True) # 业务日期

    def __repr__(self):
        return "".format(self.TRADINGDAY, self.INSTRUMENTID)

    __str__ = __repr__


class Categoryinfo(models.Model):
    class Meta:
        db_table = 'categoryinfo'

    EUTIME = models.CharField(max_length=50, null=True)
    TRANSCODE = models.CharField(max_length=10, null=True)
    TRANSETYPE = models.CharField(max_length=20, null=True)
    MARKETCODE = models.CharField(max_length=20, null=True)
    MARKET = models.CharField(max_length=20, null=True)
    LISTINGSTATE = models.CharField(max_length=20, null=True)
    TRANSUNIT = models.CharField(max_length=30, null=True)
    PRICEUNIT = models.CharField(max_length=30, null=True)
    MINPCHANGE = models.CharField(max_length=30, null=True)
    CONTRADATE = models.CharField(max_length=50, null=True)
    TRANSDATE = models.CharField(max_length=200, null=True)
    LTRANSDATE = models.CharField(max_length=100, null=True)
    DELIVERYDATE = models.CharField(max_length=100, null=True)
    TRANSMARGIN = models.CharField(max_length=20, null=True)
    PRICELIMIT = models.CharField(max_length=100, null=True)
    DELIVLOACT = models.CharField(max_length=50, null=True)
    DELIVMETHOD = models.CharField(max_length=50, null=True)
    DELIVGRADE = models.CharField(max_length=500, null=True)
    TRANSFEE = models.CharField(max_length=50, null=True)
    DELIVUNIT = models.CharField(max_length=50, null=True)
    MINDUNIT = models.CharField(max_length=50, null=True)
    CURRENCY = models.CharField(max_length=20, null=True)
    CONTRTYPE = models.CharField(max_length=20, null=True)
    CONTRSUBTYPE = models.CharField(max_length=30, null=True)
    HYCS = models.CharField(max_length=20, null=True)
    ZXDBJ = models.CharField(max_length=20, null=True)
    BZJB = models.CharField(max_length=20, null=True)

class MainContract(models.Model):
    class Meta:
        db_table = 'maincontract'

    category = models.CharField(max_length=10, null=True)
    symbol = models.CharField(max_length=20, null=True)
    instrumentId = models.CharField(max_length=20, null=True)
    tradingDay = models.CharField(max_length=30, null=True)


class ExchangeDate(models.Model):
    class Meta:
        db_table = 'exchange_date'

    INIT_DATE = models.CharField(max_length=20, null=True)