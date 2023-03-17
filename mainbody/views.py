from django import forms
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import password_validators_help_text_html,validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import login as Login
from django.contrib.auth import logout as Logout
from django.contrib import messages
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from .models import check_out
import sqlite3

class HomeListView(ListView):
    model = check_out
    def get_asset_data(self,**kwargs):
        context = super(HomeListView,self).get_context_data(**kwargs)
        return context 

# Below is the authentiation part when logging in.
def login(request):
    if request.method == "GET":
        return render(request,'user/login.html')
    if request.method == "POST":
        loginname = request.POST['username']
        loginpass = request.POST['password']
        user = authenticate(request,username=loginname, password=loginpass)#verificate in the database
        if user is not None:
            Login(request,user)
            return HttpResponseRedirect('/')
        else:
            messages.error(request,'Wrong user name or password, try again.')
            return HttpResponseRedirect('/login/')

@login_required(login_url='/login/')
def logout(request):
    Logout(request)
    messages.success(request,'Logged out sucessfully!')
    return HttpResponseRedirect('/login/')

@login_required(login_url='/login/')
def homepage(request):
    queryset = list(check_out.objects.filter(userID=request.user.id).values_list("asset","checkdate"))
    return render(request,'user/home.html',{"queryset":queryset,"Username":request.user.username})

# Below is the functions controls password changes
@login_required(login_url='/login/')
def passwordchange(request):
    if request.method == 'GET':
        return render(request,'user/passchange.html',{'inquiry':password_validators_help_text_html(),"Username":request.user.username})
    if request.method == 'POST':
        user = request.user.username #user name for verificate
        oldpass = request.POST.get('oldpass') #Original password
        newpassorigin = request.POST.get('newpass0') #Set new password
        newpassverifi = request.POST.get('newpass1') #Input new password again to verificate
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        if authenticate(username=f'{user}', password=f'{oldpass}') is not None: #database verification passed
            if newpassorigin == newpassverifi:
                if validate_password(newpassorigin) != []:
                    messages.error(request,'One or more requirements not satisfied. Try again.')
                    return HttpResponseRedirect('/change_password/')
                from django.contrib.auth.hashers import make_password
                newpassencrypt = make_password(f'{newpassorigin}')
                cursor.execute(f'UPDATE auth_user SET password=\'{newpassencrypt}\' WHERE username =\'{user}\';')
                conn.commit()
                messages.success(request,'Your password has been changed.')
                return HttpResponseRedirect('/')
            else:
                messages.error(request,'Different new passwords. Try again.')
                return HttpResponseRedirect('/change_password/')
        else:
            messages.error(request,"Password incorrect. Try again")
            return HttpResponseRedirect('/change_password/')

@login_required(login_url='/login/')
def manageinf(request):
    if request.method == 'GET':
        user = request.user.username
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        queryset = cursor.execute(f'SELECT username,email,first_name,last_name,last_login FROM auth_user WHERE username = \'{user}\'')
        inflist = ["username","email","first_name","last_name","last login time"]
        return render(request,'user/changeinf.html',{'queryset':queryset,"infolist":inflist,"Username":request.user.username})
    if request.method == 'POST':
        print(request.POST.get("username"))
        user = request.user.username
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        print([request.POST.get("email"),request.POST.get("firstname"),request.POST.get("lastname"),request.POST.get("username")])
        if [request.POST.get("email"),request.POST.get("firstname"),request.POST.get("lastname"),request.POST.get("username")] == ['','','','']:
            messages.error(request,"You need to change at least one information!")
            return HttpResponseRedirect('/manage_inf/')
        
        if request.POST.get("email") != '': 
            email = request.POST.get("email")                                                                   # First is to check if the user has changed the info
            cursor.execute(f"UPDATE auth_user SET email=\'{email}\' WHERE username = \'{user}\'")               # (detailed in if argument)
        if request.POST.get("firstname") != '':   
            firstname = request.POST.get("firstname")                                                           # Second is to control database to change the info 
            cursor.execute(f"UPDATE auth_user SET first_name=\'{firstname}\' WHERE username = \'{user}\'")      # specified.
        if request.POST.get("lastname") != '':                                                                  # (via cursor function in sqlite3 pack with python)
            lastname = request.POST.get("lastname")
            cursor.execute(f"UPDATE auth_user SET last_name=\'{lastname}\' WHERE username = \'{user}\'")
        
        # change username
        status = True                                                                                           # Change user name is unique because:
        for item in list(cursor.execute("SELECT username FROM auth_user")):                                     # 1. Above three db executions depend on the username column in table.
            if request.POST.get("username") in item:                                                            # 2. username in database should be UNIQUE so there should be                                                                                      
                break                                                                                           #    exists in database. That's through a status bool variable and a for progress.
        if request.POST.get("username") != '' and status:                                                       #    if new username confilcts, status should be false.
            username = request.POST.get("username")                                                             # 3. After username is changed, assets in table check_out should also change
            cursor.execute(f"UPDATE auth_user SET username=\'{username}\' WHERE username = \'{user}\'")         #    corresponding usernames.
            cursor.execute(f"UPDATE mainbody_check_out SET user=\'{username}\' WHERE user = \'{user}\'") 
        else:
            messages.error(request,'User name already exists. Try another name.')
            return HttpResponseRedirect('/manage_inf/')
        
        conn.commit()
        cursor.close() #security/thread occupation concern
        messages.success(request,'Your information has been changed.')
        return HttpResponseRedirect("/")

'''@login_required(login_url='/login/')
def admin_page(request):'''


'''
                                                             _ooOoo_
                                                            o8888888o
                                                            88" . "88
                                                            (| -_- |)
                                                             O\ = /O
                                                         ____/`---'\____
                                                       .   ' \\| |// `.
                                                        / \\||| : |||// \
                                                      / _||||| -:- |||||- \
                                                        | | \\\ - /// | |
                                                      | \_| ''\---/'' | |
                                                       \ .-\__ `-` ___/-. /
                                                    ___`. .' /--.--\ `. . __
                                                 ."" '< `.___\_<|>_/___.' >'"".
                                                | | : `- \`.;`\ _ /`;.`/ - ` : | |
                                                  \ \ `-. \_ __\ /__ _/ .-` / /
                                          ======`-.____`-.___\_____/___.-`____.-'======
                                                             `=---='

                                    寫字樓裡寫字間，寫字間裡程序員；程式人員寫程序，又拿程序換酒錢。
                                    酒醒只在網上坐，酒醉還來網下眠；酒醉酒醒日復日，網上網下年復年。
                                    寧願老死程序間，只要老闆多發錢；小車大房不去想，撰個二千好過年。
                                    若要見識新世面，公務員比程序員；一個在天一在地，而且還比我們閒。
                                    別人看我穿白領，我看別人穿名牌；天生我才寫程序，臀大近視肩周炎。

                                    年復一年春光度，度得他人做老闆；老闆扣我薄酒錢，沒有酒錢怎過年。
                                    春光逝去皺紋起，作起程序也委靡；來到水源把水灌，打死不做程序員。
                                    別人笑我忒瘋癲，我笑他人命太賤；狀元三百六十行，偏偏來做程序員。
                                    但願老死電腦間，不願鞠躬老闆前；奔馳寶馬貴者趣，公交自行程序員。
                                    別人笑我忒瘋癲，我笑自己命太賤；不見滿街漂亮妹，哪個歸得程序員。

                                    不想只掙打工錢，那個老闆願發錢；小車大房咱要想，任我享用多悠閒。
                                    比爾能搞個微軟，我咋不能撈點錢；一個在天一在地，定有一日乾坤翻。
                                    我在天來他在地，縱橫天下山水間；傲視武林豪傑墓，一樽還壘風月山。
                                    電腦面前眼發直，眼鏡下面淚茫茫；做夢發財好幾億，從此不用手指忙。
                                    哪知夢醒手空空，老闆看到把我訓；待到老時眼發花，走路不知哪是家。

                                    小農村裡小民房，小民房裡小民工；小民工人寫程序，又拿代碼討賞錢。
                                    錢空只在代碼中，錢醉仍在代碼間；有錢無錢日復日，碼上碼下年復年。
                                    但願老死代碼間，不願鞠躬奧迪前，奧迪奔馳貴者趣，程序代碼貧者緣。
                                    若將貧賤比貧者，一在平地一在天；若將貧賤比車馬，他得驅馳我得閒。
                                    別人笑我忒瘋癲，我笑他人看不穿；不見蓋茨兩手間，財權富貴世人鑒。
'''  