from django.http import JsonResponse, HttpRequest, HttpResponse, HttpResponseBadRequest
from .models import User, Book, Tick_1min, Categoryinfo
import simplejson
from django.forms.models import model_to_dict
import re
import time

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
        if b[0].password == password:  # 密码成功匹配
            try:
                if userName:
                    request.session['userName'] = userName
                if password:
                    request.session['password'] = password
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
    user.password = data['password']
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
    userName = data['value']
    print("userName=", userName)
    mgr = User.objects

    user = mgr.filter(userName = userName)

    if user: # 说明存在
        return JsonResponse({'userNameMsg': 'illegal'})
    else: # 说明不存在
        return JsonResponse({'userNameMsg': 'legal'})

def currentUser(request):
    userName = request.session.get('userName')
    json_dict = {}
    try:
        user = User.objects.get(userName = userName)
        json_dict = model_to_dict(user)
        return JsonResponse(json_dict)
    except:
        return JsonResponse(json_dict)


def getUserInfoById(request):
    data = simplejson.loads(request.body)
    if data:
        print("data=",data)
        userId = data['userId']
        try:
            user = User.objects.get(userId=userId)
            json_dict = model_to_dict(user)
            return JsonResponse(json_dict)
        except:
            return JsonResponse({})
    else:
        return JsonResponse({})


def queryNextTick1MinData(request):
    data = simplejson.loads(request.body)
    orderCount = data['orderCount']

    if orderCount < 10:
        json_list = queryTick1Min(150 + orderCount + 1)
        msg = {"isOver": False, "json_list": json_list}
    else:
        json_list = queryTick1Min(161)
        msg = {"isOver": True, "json_list": json_list}
    return JsonResponse(msg, safe=False)

def queryNextTick1MinData2(request):
    # time.sleep(3)
    data = simplejson.loads(request.body)
    orderCount = data['orderCount']
    profitInPosition = 0 # 本次下单的持仓盈亏
    profitInClosePosition = 0 # 本次下单的平仓盈亏

    if data['isOrder'] and data['nextTick'] and data['lastTick'] and orderCount <= 10: # 开始计算盈亏

        transUnit = data['transUnit'] # 获得合约乘数
        transMargin = data['transMargin']# 获得保证金比

        nextTick = data['nextTick']
        openOrClose = data['openOrClose'] # 开平方向
        direction = data['direction'] # 买卖方向
        orderPrice = data['price']  # 下单价格
        num = data['num']  # 手数
        contrastPrice = nextTick[2]  # 最新价/收盘价

        if openOrClose == '1' and direction == '1': # 买开,则最新价 - 开仓价
            profitInPosition = (contrastPrice - orderPrice)*num # 持仓盈亏

        elif openOrClose == '1' and direction == '2': # 卖开,则开仓价 - 最新价
            profitInPosition = (orderPrice - contrastPrice)*num # 持仓盈亏

        if openOrClose == '2' and direction == '1': # 买平,则用 开仓价 - 平仓价
            openPositionPrice = data['openPositionPrice'] # 开仓价
            profitInClosePosition = (openPositionPrice - orderPrice)*num # 平仓盈亏

        elif openOrClose == '2' and direction == '2': # 卖平,则用 平仓价 - 开仓价
            openPositionPrice = data['openPositionPrice']  # 开仓价
            profitInClosePosition = (orderPrice - openPositionPrice)*num # 平仓盈亏
        profitInPosition = profitInPosition*transUnit
        profitInClosePosition = profitInClosePosition*transUnit

    elif data['isWatch'] and data['positionNum'] > 0 and orderCount <= 10: # 点击观望，若有持仓，需要计算浮动盈亏

        transUnit = data['transUnit']  # 获得合约乘数
        transMargin = data['transMargin']  # 获得保证金比

        num = data['num']  # 手数
        direction = data['direction']  # 买卖方向
        nextTick = data['nextTick']
        contrastPrice = nextTick[2]  # 最新价/收盘价
        openPositionPrice = data['openPositionPrice']  # 开仓价

        if direction == '1':
            profitInPosition = (contrastPrice - openPositionPrice)*num # 持仓盈亏
        elif direction == '2':
            profitInPosition = (openPositionPrice - contrastPrice)*num  # 持仓盈亏
        profitInPosition = profitInPosition*transUnit

    if orderCount < 10:
        json_list = queryTick1Min(150 + orderCount + 1)
        msg = {"isOver": False, "profitInPosition": profitInPosition, "profitInClosePosition": profitInClosePosition, "json_list": json_list}
    else:
        json_list = queryTick1Min(161)
        msg = {"isOver": True, "profitInPosition": profitInPosition, "profitInClosePosition": profitInClosePosition, "json_list": json_list}
    return JsonResponse(msg, safe=False)


def calculateProfit(request):
    data = simplejson.loads(request.body)
    print("data=", data)
    if data:
        userId = data['userId']
        profitInPosition = data['profitInPosition']
        profitInClosePosition = data['profitInClosePosition']
        bond = data['bond']
        availableFund = data['availableFund']
        currentInterest = data['currentInterest']
        user = User.objects.get(userId=userId)
        user.profitInPosition = profitInPosition
        user.profitInClosePosition += profitInClosePosition
        user.bond += bond
        user.currentInterest = currentInterest
        user.availableFund = availableFund
        user.save()
        return JsonResponse({"status": "ok"}, safe=False)
    else:
        return JsonResponse({"status": "error"}, safe=False)


def queryTick1Min(num):
    mgr = Tick_1min.objects
    qs = mgr.values_list('TRADINGDAY','OPENPRICE','CLOSEPRICE','LOWESTPRICE','HIGHESTPRICE','VOLUME','UPDATETIME',
                         flat=False).filter(TRADINGDAY='20191014',INSTRUMENTID='ag1912').order_by('TRADINGDAY','UPDATETIME')[:num]

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
    json_list = queryAllCategoryList()
    return JsonResponse(json_list, safe=False)

def queryAllCategoryList():
    mgr = Categoryinfo.objects
    qs = mgr.all()

    json_list = []
    for category in qs:
        json_dict = model_to_dict(category)
        json_list.append(json_dict)
    return json_list




