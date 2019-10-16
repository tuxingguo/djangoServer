from django.http import JsonResponse, HttpRequest, HttpResponse, HttpResponseBadRequest
from .models import User, Book
import simplejson
from django.forms.models import model_to_dict

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
        print('json_dict=', json_dict)
        return JsonResponse(json_dict)
    except:
        return JsonResponse(json_dict)

# def queryTickData(request):
#     json_list = querytick()
#     return JsonResponse(json_list, safe=False)
#
# def querytick():
#     mgr = Book.objects
#     qs = mgr.all()
#
#     json_list = []
#     for book in qs:
#         json_dict = model_to_dict(book)
#         json_list.append(json_dict)
#     return json_list