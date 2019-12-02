from django.http import JsonResponse, HttpRequest, HttpResponse, HttpResponseBadRequest
from .models import User, Book, Tick_1min, Categoryinfo, MainContract, ExchangeDate
import simplejson
from django.forms.models import model_to_dict
import re
import datetime
import random
import math
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password

def write_myApp(request):
    data = simplejson.loads(request.body)
    userId = data['userId']
    userName = data['userName']

    print("userId=", userId, "   userName=", userName)

    user = User()
    user.userId = userId
    user.userName = userName

    try:
        user.save()  # 自动提交
        return JsonResponse({"success": True})
    except Exception as e:
        return HttpResponseBadRequest()

def search(request):

    mgr = User.objects
    qs = mgr.all()

    print("qs=", qs.query)

    json_list = []
    for user in qs:
        json_dict = model_to_dict(user)
        json_list.append(json_dict)
    return JsonResponse(json_list, safe=False)

def save(request):
    data = simplejson.loads(request.body)
    print("user:", data['item'])

    user = data['item']
    name = user["name"]
    age = user["age"]
    email = user["email"]

    user = User()
    user.name = name
    user.age = age
    user.email = email

    try:
        user.save()
        return JsonResponse({"success": True})
    except Exception as e:
        print("e=", e)
        return HttpResponseBadRequest()

def getUserById(request):
    data = simplejson.loads(request.body)
    print("id=", data["id"])
    id = data["id"]
    mgr = User.objects

    try:
        user = mgr.get(id=id)

        resp_user = model_to_dict(user)

        print("resp_user=", resp_user)

        return JsonResponse(resp_user, safe=False)
    except Exception as e:
        print("e=", e)
        return HttpResponseBadRequest()


def update(request):
    data = simplejson.loads(request.body)
    item  = data['item']

    print("item:", item)

    userId = item['id']
    name = item['name']
    age = item["age"]
    email = item['email']

    user = User()
    user.id = userId
    user.name = name
    user.age = age
    user.email = email

    try:
        user.save()
        return JsonResponse({"success": True})
    except Exception as e:
        print("e=", e)
        return HttpResponseBadRequest()

def deleteById(request):
    data = simplejson.loads(request.body)
    id = data["id"]
    try:
        if id:
            userObj = User.objects.get(id = id)
            userObj.delete()
            return JsonResponse({"success": True})
    except Exception as e:
        print("e=", e)
        return HttpResponseBadRequest()


def queryBook(request):
    json_list = queryAllBook()
    return JsonResponse(json_list, safe=False)

def addBook(request):
    data = simplejson.loads(request.body)
    print("data:", data)

    bookName = data['bookName']
    author = data['author']
    price = data['price']
    publish = data['publish']

    try:
        if price:
            price = float(price)

        book = Book()
        book.bookName = bookName
        book.author = author
        book.price = price
        book.publish = publish
        book.save()
    except Exception as e:
        print("e=", e)
        return HttpResponseBadRequest()

    try:
        json_list = queryAllBook()
        return JsonResponse(json_list, safe=False)
    except Exception as e:
        print("e=", e)
        return HttpResponseBadRequest()

def deleteBook(request):
    data = simplejson.loads(request.body)
    print("data_del:", data)
    id = data["id"]
    try:
        if id:
            bookObj = Book.objects.get(id = id)
            bookObj.delete()
            json_list = queryAllBook()
            return JsonResponse(json_list, safe=False)
    except Exception as e:
        print("e=", e)
        return HttpResponseBadRequest()


def updateBook(request):
    data = simplejson.loads(request.body)
    print("data=", data)

    id = data['id']
    bookName = data['bookName']
    author = data["author"]
    price = data['price']
    publish = data['publish']

    book = Book()
    book.id = id
    book.bookName = bookName
    book.author = author
    book.price = price
    book.publish = publish

    try:
        book.save()
        json_list = queryAllBook()
        return JsonResponse(json_list, safe=False)
    except Exception as e:
        print("e=", e)
        return HttpResponseBadRequest()

def queryAllBook():
    mgr = Book.objects
    qs = mgr.all()

    json_list = []
    for book in qs:
        json_dict = model_to_dict(book)
        json_list.append(json_dict)
    return json_list


## *********************************************************************************

def account(request):
    data = simplejson.loads(request.body)
    print("data=", data)
    userName = data['userName']
    password = data['password']

    b = User.objects.filter(userName=userName)
    a = len(b)
    if a == 0:
        return JsonResponse({"status":"fail","type":"account","currentAuthority":"guest"}, safe=False)

    else:
        if check_password(password, b[0].password):  # 密码成功匹配
            try:
                if userName:
                    request.session['userName'] = userName
                    request.session['userId'] = b[0].userId
            except:
                pass
            return JsonResponse({"status": "ok", "type": "account", "currentAuthority": "admin"}, safe=False)
        else:   # 密码错误
            return JsonResponse({"status": "fail", "type": "account", "currentAuthority": "guest"}, safe=False)

def register(request):
    data = simplejson.loads(request.body)
    print("data:", data)

    user = User()
    user.userName = data['userName']
    user.email = data['email']
    if len(data['password']) <  10:
        user.PwdStrength = 'middle'
    elif len(data['password']) >= 10:
        user.PwdStrength = 'strong'
    user.password = make_password(data['password'])
    user.avatar = 'avatar.png'
    user.InitialInterest = 1000000 # 设置期初权益
    user.bond = 0 # 保证金
    user.profitInPosition = 0 # 浮动盈亏
    user.profitInClosePosition = 0 # 平仓盈亏
    user.currentInterest = 1000000 # 当前权益
    user.availableFund = 1000000 # 可用资金
    try:
        user.save()
        jsonObj = { 'status': 'ok', 'currentAuthority': 'user' }
        return JsonResponse(jsonObj)
    except Exception as e:
        print("e=", e)
        jsonObj = {'status': 'fail', 'currentAuthority': 'guest'}
        return JsonResponse(jsonObj)


def checkUserName(request):
    data = simplejson.loads(request.body)
    if 'value' in data:
        userName = data['value']
        print("userName=", userName)
        mgr = User.objects

        user = mgr.filter(userName = userName)

        if user: # 说明存在
            return JsonResponse({'userNameMsg': 'illegal'})
        else: # 说明不存在
            return JsonResponse({'userNameMsg': 'legal'})
    else:
        return JsonResponse({'userNameMsg': 'legal'})

def currentUser(request):
    userId = request.session.get('userId')
    json_dict = {}
    try:
        user = User.objects.get(userId = userId)
        json_dict = model_to_dict(user)
        return JsonResponse(json_dict)
    except:
        return JsonResponse(json_dict)


def getUserInfoById(request):
    data = simplejson.loads(request.body)
    if 'userId' in data:
        userId = data['userId']
    else:
        userId = request.session.get('userId')

    try:
        user = User.objects.get(userId=userId)
        json_dict = model_to_dict(user)
        return JsonResponse(json_dict)
    except:
        return JsonResponse({})



exerciseCount = 10 # 每一次测试跳动K线数
# kLineNum = 150 # 初始加载K线数



def getdate(beforeOfDay):
    today = datetime.datetime.now()
    # 计算偏移量
    offset = datetime.timedelta(days=-beforeOfDay)
    # 获取想要的日期的时间
    re_date = (today + offset).strftime('%Y%m%d')
    return re_date

# 获取前一周的所有日期(weeks=1)，获取前N周的所有日期(weeks=N)
def getBeforeWeekDays(weeks=1):
    # 0,1,2,3,4,5,6,分别对应周一到周日
    week = datetime.datetime.now().weekday()
    days_list = []
    start = 7 * weeks +  week
    end = week
    for index in range(start, end, -1):
        day =getdate(index)
        days_list.append(day)
    return days_list

def queryOriginTickData(request):
    data = simplejson.loads(request.body)
    transCode = data['transCode'] # 合约品种

    tradingDayList = []
    # days_list = getBeforeWeekDays()
    days_list = []
    days_list.append('20191125')
    days_list.append('20191126')
    days_list.append('20191127')
    days_list.append('20191128')
    days_list.append('20191129')
    days_list.append('20191130')
    days_list.append('20191201')

    for day in days_list:
        exchangeDate = ExchangeDate.objects.filter(INIT_DATE=day)
        if exchangeDate:
            tradingDayList.append(exchangeDate[0].INIT_DATE)
    print("tradingDayList=", tradingDayList)

    length = len(tradingDayList) # length 4
    index = random.randint(0, length-1) # 产生随机数0、1、2、3
    tradingDay = tradingDayList[index] # 交易日确定

    print("随机交易日=", tradingDay)

    # 首先根据当前日期，取出上一周，然后对比交易日表，拿到上一周所有的交易日，然后随机选一天，以此确定交易日期
    # 根据交易日期、合约品种，即可获得主力合约号

    mainContractOB = MainContract.objects.filter(category=transCode, tradingDay=tradingDay)
    mainContract = mainContractOB[0].instrumentId  # 主力合约号确定
    print("主力合约号=", mainContract)

    count = Tick_1min.objects.filter(TRADINGDAY=tradingDay,INSTRUMENTID=mainContract).count()
    print("总条数=", count)

    kLineNum = math.floor(count * 0.5)
    print("kLineNum=", kLineNum)
    if count < 23:
        start = 0
        end = count

    else:
        start = random.randint(0, count - kLineNum - exerciseCount - 1)
        end = start + kLineNum


    print("k线区间=[", start ,",", end ,"]")

    json_list = queryTick1Min(mainContract, tradingDay, start, end + 1)
    msg = {"isOver": False, "mainContract": mainContract, "json_list": json_list, "start": start, "end": end, "tradingDay": tradingDay}

    return JsonResponse(msg, safe=False)



def queryNextTick1MinData(request):
    global exerciseCount
    data = simplejson.loads(request.body)

    # print("现在时刻1:", datetime.datetime.now())

    orderCount = data['orderCount']
    tradingDay = data['tradingDay'] # 日期
    start = data['start']
    end = data['end']
    mainContract = data['mainContract']

    print("mainContract=", mainContract)
    if orderCount < exerciseCount:
        json_list = queryTick1Min(mainContract, tradingDay, start, end + orderCount + 1)
        msg = {"isOver": False, "mainContract": mainContract, "json_list": json_list, "start": start, "end": end, "tradingDay": tradingDay}
    else:
        json_list = queryTick1Min(mainContract, tradingDay, start, end+exerciseCount+1)
        msg = {"isOver": True, "mainContract": mainContract, "json_list": json_list, "start": start, "end": end, "tradingDay": tradingDay}

    # print("现在时刻2:", datetime.datetime.now())
    return JsonResponse(msg, safe=False)



def getMainContract(tradingDay, transCode): # 根据品种和时间，获取主力合约
    mgr = MainContract.objects
    mainContractOB = mgr.get(category=transCode, tradingDay=tradingDay)
    instrumentId = mainContractOB.instrumentId
    return instrumentId

def calculateProfit(request):
    data = simplejson.loads(request.body)
    print("data=", data)
    if data:
        userId = data['userId']
        user = User.objects.get(userId=userId)

        if 'profitInPosition' in data:
            profitInPosition = data['profitInPosition']
            user.profitInPosition = profitInPosition  # 覆盖持仓盈亏

        if 'profitInClosePosition' in data:
            profitInClosePosition = data['profitInClosePosition']
            user.profitInClosePosition = profitInClosePosition  # 叠加平仓盈亏

        if 'bond' in data:
            bond = data['bond']
            user.bond = bond

        if 'availableFund' in data:
            availableFund = data['availableFund']
            user.availableFund = availableFund

        if 'currentInterest' in data:
            currentInterest = data['currentInterest']
            user.currentInterest = currentInterest

        user.save()
        return JsonResponse({"status": "ok"}, safe=False)
    else:
        return JsonResponse({"status": "error"}, safe=False)


def queryTick1Min(mainContract,tradingDay, start, num):
    mgr = Tick_1min.objects
    qs = mgr.values_list('ACTIONDAY','OPENPRICE','CLOSEPRICE','LOWESTPRICE','HIGHESTPRICE','VOLUME','UPDATETIME',
                         flat=False).filter(TRADINGDAY=tradingDay,INSTRUMENTID=mainContract).order_by('ACTIONDAY','TRADINGDAY','UPDATETIME')[start:num]

    qs = list(qs)
    return qs


def getCatgoryInfo(TRANSCODE):  # 传入品种，大写
    categoryInfo = {}
    mgr = Categoryinfo.objects
    dict =  mgr.values('TRANSCODE', 'TRANSETYPE','TRANSUNIT', 'TRANSMARGIN').filter(TRANSCODE = TRANSCODE) # 品种  类型  合约乘数  保证金比
    if dict:
        categoryInfo = dict[0]
        categoryInfo['TRANSUNIT'] = re.sub('[\u4e00-\u9fa5,/]', '', categoryInfo['TRANSUNIT'])
        categoryInfo['TRANSMARGIN'] = re.sub('[\u4e00-\u9fa5]', '', categoryInfo['TRANSMARGIN'])
    return categoryInfo


def getKind(instrumentID): # 得到品种
    kind = re.sub("[0-9]", " ", instrumentID)
    kind = kind.upper()
    return  kind


def queryCategoryList(request): # 得到品种列表
    data = simplejson.loads(request.body)
    keyWord = None
    if "key" in data:
        keyWord = data["key"]
    json_list = queryAllCategoryList(keyWord)
    return JsonResponse(json_list, safe=False)

def queryAllCategoryList(keyWord):
    mgr = Categoryinfo.objects
    qs = mgr.filter(Q(TRANSCODE__icontains=keyWord) | Q(TRANSETYPE__icontains=keyWord))

    json_list = []
    for category in qs:
        json_dict = model_to_dict(category)
        json_list.append(json_dict)
    return json_list

# 修改基本信息
def updateMyInfo(request):
    data = simplejson.loads(request.body)
    print("data=", data)

    userId = data['userId']
    userName = data['userName']
    email = data['email']
    profile = data['profile']

    try:
        User.objects.filter(userId=userId).update(userName=userName, email=email,profile=profile)
        return JsonResponse({'status': 200})
    except Exception as e:
        return JsonResponse({'status': 500})

# 修改密码
def updatePassword(request):
    data = simplejson.loads(request.body)
    print("data=", data)

    userId = data['userId']
    password = data['password']

    PwdStrength = 'middle' if len(password) < 10 else 'strong'

    try:
        mpwd = make_password(password)
        User.objects.filter(userId=userId).update(password=mpwd, PwdStrength=PwdStrength)
        return JsonResponse({'status': 200})
    except Exception as e:
        return JsonResponse({'status': 500})

def updateMyFund(request):
    data = simplejson.loads(request.body)
    userId = data['userId']
    fund = data['fund']
    mgr = User.objects

    user = mgr.get(userId=userId)
    availableFund = user.availableFund + fund
    currentInterest = user.currentInterest + fund

    try:
        User.objects.filter(userId=userId).update(availableFund = availableFund, currentInterest = currentInterest)
        return JsonResponse({'status': 200})
    except Exception as e:
        return JsonResponse({'status': 500})

def checkOldPassword(request):
    data = simplejson.loads(request.body)
    userId = data['userId']
    pwd = data['value']

    user = User.objects.filter(userId=userId)

    if check_password(pwd, user[0].password):  # 密码成功匹配
        return JsonResponse({'pwd_bool': True})
    else:
        return JsonResponse({'pwd_bool': False})