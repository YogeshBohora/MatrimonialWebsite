from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import *
import datetime
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Create your views here.
def Home(request):
    sign=Signup.objects.all()
    pro = Profile.objects.all()
    error=False
    if request.user:
        error=True
    try:
        pro = Profile.objects.all()
        user = User.objects.get(id=request.user.id)
        sign = Signup.objects.get(user=user)
        for i in pro:
            i.age = datetime.date.today().year - i.signup.dob.year
            i.save()
    except:pass
    d = {'pro': pro, 'sign': sign,'error':error}
    return render(request, 'user_home.html', d)


def About(request):
    num = [1]
    d = {'success':[],'num':num}
    return render(request,'about.html',d)


def Contact(request):
    return render(request,'contact.html')


def Signup_User(request):
    error = False
    religion = Religion.objects.all()
    if request.method == 'POST':
        fields = ['fname','lname','uname','pwd','email','contact','date','city','add','religion','quali','gen']
        f_mapping = {
            'fname':'First Name',
            'lname':'Last Name',
                        'uname':'Username',
                        'pwd':'Password','date':'Date of Birth','city':'City',
                        'add':'Address','email':'Email','gen':'Gender','contact':'Contact Number',
            'religion':'Religion',
            'quali': 'Qualification'
        }
        print(request.POST['religion'])
        for field in fields:
            if not field in request.POST or request.POST[field]==None or request.POST[field]=='':
                return render(request,'signup.html', {'values':request.POST,'focus_field':field,'religion':religion,'message': 'Sorry, {} is required.'.format(f_mapping[field])})
        if not 'img' in request.FILES or request.FILES['img'] == None:
            return render(request,'signup.html', {'values':request.POST,'focus_field':'img','religion':religion,'message': 'Sorry, {} is required.'.format('Image')})
        if User.objects.filter(username=request.POST['uname']).exists():
            return render(request,'signup.html', {'values':request.POST,'focus_field':'uname','religion':religion,'message': 'Sorry, user with username {} already exists.'.format(request.POST['uname'])})
        if User.objects.filter(email=request.POST['email']).exists():
            return render(request,'signup.html', {'values':request.POST,'focus_field':'email','religion':religion,'message': 'Sorry, user with email {} already exists.'.format(request.POST['email'])})

        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['uname']
        p = request.POST['pwd']
        d = request.POST['date']
        c = request.POST['city']
        ad = request.POST['add']
        e = request.POST['email']
        i = request.FILES['img']
        g = request.POST['gen']
        con = request.POST['contact']
        quali = request.POST['quali']
        reli = request.POST['religion']
        print(religion)
        user = User.objects.create_user(username=u, email=e, password=p, first_name=f,last_name=l)
        status = Status.objects.get(status="pending") if Status.objects.filter(status="pending").exists() else Status.objects.create(status="pending")
        sign = Signup.objects.create(user=user,status=status ,dob=d, city=c, address=ad, contact=con,image=i,gen=g)
        Profile.objects.create(signup = sign,qualification=quali,religion=Religion.objects.get(religion=reli))
        return render(request,'login.html', {'error': "success"})
        error = True
    d = {'error':error,'religion':religion}
    return render(request, 'signup.html',d)

def Login(request):
    error = ""
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        if user:
            if user.is_staff:
                login(request, user)
                return render(request,'login.html',{'error':"admin"})
            sign = Signup.objects.get(user=user)
        else:
            error="not"
        try:
            if sign.status.status == "pending":
                error="pending"
            elif sign.status.status == "Reject":
                error="reject"
            else:
                if user:
                    login(request, user)
                    error = "yes"
                else:
                    error = "not"

        except:
            error="not"
    context = {'error': error}
    return render(request,'login.html',context)




def Logout(request):
    logout(request)
    return redirect('home')

def Admin_Home(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    sign = Signup.objects.all()
    pro = Religion.objects.all()
    total_gents = 0
    total_lady = 0
    total_religion = 0
    for i in sign:
        if i.gen == "male":
            total_gents+=1
        if i.gen == "female":
            total_lady+=1
    for i in pro:
        total_religion+=1
    d = {'total_gents':total_gents,'total_lady':total_lady,'total_religion':total_religion}
    return render(request,'admin_home.html',d)


def cosine_similarity(x_list,y_list):
    X_list = word_tokenize(x_list)
    Y_list = word_tokenize(y_list)
    sw = stopwords.words('english')
    l1 =[];l2 =[]
    X_set = {w for w in X_list if not w in sw}
    Y_set = {w for w in Y_list if not w in sw}
    rvector = X_set.union(Y_set)
    for w in rvector:
        if w in X_set: l1.append(1) # create a vector
        else: l1.append(0)
        if w in Y_set: l2.append(1)
        else: l2.append(0)
    c = 0

    # cosine formula
    for i in range(len(rvector)):
        c+= l1[i]*l2[i]
    cosine = c / float((sum(l1)*sum(l2))**0.5)
    return cosine


def View_Customer_Api(request):
    users_res = []
    users = User.objects.all()
    for user in users:
        if not user.is_superuser:
            sign = Signup.objects.get(user=user)
            pro = Profile.objects.exclude(signup__gen=sign.gen)
            user_profile = Profile.objects.get(signup=sign)
            user_profile.age = datetime.date.today().year - user_profile.signup.dob.year
            user_profile.save()
            X_list = [user_profile.signup.city,user_profile.qualification if user_profile.qualification else "", user_profile.religion.religion if user_profile.religion is not None else ""]
            profiles = []

            for profile in pro:
                profile.age = datetime.date.today().year - profile.signup.dob.year
                profile.save()
                if not request.GET.get('a'):
                    Y_list =[profile.signup.city, profile.qualification if profile.qualification else "", profile.religion.religion if profile.religion is not None else ""]
                    cosine = cosine_similarity(" ".join(X_list)," ".join(Y_list))
                    # print("similarity: ", cosine,cosine>0.5)
                    if cosine > 0.5 and profile.age> user_profile.age-2 and profile.age < user_profile.age+2:
                        prof = {}
                        all_fields = [e.name for e in Profile._meta.get_fields()]
                        prof['user'] = profile.signup.user.first_name + ' ' + profile.signup.user.last_name
                        prof['similarity'] = round(cosine*100,2)
                        profiles.append(prof)
            users_res.append({
                'fname': user.first_name,
                'lname': user.last_name,
                'profile': profiles
            })
    from django.http import response
    import json
    data = json.dumps({'data':users_res})
    return response.HttpResponse(data)





def View_Customer(request):
    if not request.user.is_authenticated:
        return redirect('login_user')

    user = User.objects.get(id=request.user.id)
    sign = Signup.objects.get(user=user)
    pro = Profile.objects.exclude(signup__gen=sign.gen)
    user_profile = Profile.objects.get(signup=sign)
    user_profile.age = datetime.date.today().year - user_profile.signup.dob.year
    user_profile.save()
    X_list = [user_profile.signup.city,user_profile.qualification if user_profile.qualification else "", user_profile.religion.religion if user_profile.religion is not None else ""]
    profiles = []
    for profile in pro:
        profile.age = datetime.date.today().year - profile.signup.dob.year
        profile.save()
        if not request.GET.get('a'):
            Y_list =[profile.signup.city, profile.qualification if profile.qualification else "", profile.religion.religion if profile.religion is not None else ""]
            cosine = cosine_similarity(" ".join(X_list)," ".join(Y_list))
            # print("similarity: ", cosine,cosine>0.5)
            if cosine > 0.5 and profile.age> user_profile.age-2 and profile.age < user_profile.age+2:
                prof = {}
                all_fields = [e.name for e in Profile._meta.get_fields()]
                for field in all_fields:
                    prof[field] = getattr(profile,field,None)
                prof['similarity'] = round(cosine*100,2)
                profiles.append(prof)
        # if cosine>0.5:
        #     profiles.append(i)

    d = {'pro': profiles if len(profiles)>0 else pro,'sign': sign,'is_related':len(profiles)>0,'is_rel_empty':not len(profiles)>0 and not request.GET.get('a')}
    return render(request,'view_customer.html',d)

def profile(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    user = User.objects.get(id=request.user.id)
    sign = Signup.objects.get(user=user)
    pro = Profile.objects.get(signup=sign)
    d = {'pro': pro}
    return render(request,'profile.html',d)

def Requested_User(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    pro = Profile.objects.all()
    d = {'pro': pro}
    return render(request,'requested_user.html',d)

def profile1(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    user = User.objects.get(id=pid)
    sign = Signup.objects.get(user=user)
    pro = Profile.objects.get(signup=sign)
    d = {'pro': pro}
    return render(request,'profile.html',d)

def view_profile(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_user')
    error=False
    pro = Profile.objects.get(id=pid)
    user = User.objects.get(id=request.user.id)
    sign = Signup.objects.get(user=user)
    pro1 = Profile.objects.get(signup=sign)
    if request.method == "POST":
        me = request.POST['message']
        SendMessage.objects.create(profile=pro, message1=me, send_user=user)
        error = True
    d = {'pro': pro,'error':error}
    return render(request,'view_profile.html',d)

def view_profile1(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    user = User.objects.get(id=pid)
    sign = Signup.objects.get(user=user)
    pro = Profile.objects.get(signup=sign)
    d = {'pro': pro}
    print(pro)
    return render(request,'view_profile.html',d)

def view_sent_message(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    pro=""
    try:
        user = User.objects.get(id=request.user.id)
        sign = Signup.objects.get(user=user)
        pro1 = Profile.objects.get(signup=sign)
        pro = SendMessage.objects.all()
    except:
        pass
    d = {'pro': pro}
    return render(request,'sent_message.html',d)


def view_request_message(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    pro=""
    try:
        user = User.objects.get(id=request.user.id)
        sign = Signup.objects.get(user=user)
        pro1 = Profile.objects.get(signup=sign)
        pro = SendMessage.objects.filter(profile=pro1)
    except:
        pass
    d = {'pro': pro}
    return render(request,'request_message.html',d)

def view_user(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    pro1 = Profile.objects.all().order_by('-id')
    d = {'pro': pro1}
    return render(request,'view_user.html',d)

def Add_Caste(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    error = False
    if request.method=="POST":
        c = request.POST['religion']
        Religion.objects.create(religion=c)
        error = "True"
    d = {'error':error}
    return render(request,'add_religion.html',d)

def View_Caste(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    religion = Religion.objects.all()
    d = {'religion':religion}
    return render(request,'view_religion.html',d)

def Update_profile(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    user  = User.objects.get(id=request.user.id)
    sign  = Signup.objects.get(user=user)
    pro = Profile.objects.get(signup = sign)
    religion = Religion.objects.all()
    error=False
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['uname']
        c = request.POST['city']
        ad = request.POST['add']
        e = request.POST['email']
        con = request.POST['contact']
        f_name = request.POST['f_name']
        m_name = request.POST['m_name']
        f_contact = request.POST['f_contact']
        ho = request.POST['hobby']
        w_add = request.POST['w_add']
        quali = request.POST['quali']
        sal = request.POST['salary']
        occup = request.POST['occup']
        family = request.POST['family']
        cas = request.POST['religion']
        d = request.POST['dob']
        try:
            i = request.FILES['img']
            sign.image = i
            pro.save()

        except:
            pass


        if d:
            try:
                sign.dob = d
                sign.save()
            except:
                pass
        else:
            pass
        user = User.objects.get(username=u)
        user.first_name = f
        user.last_name = l
        user.email = e
        user.save()
        sign.user = user
        sign.contact = con
        sign.address = ad
        sign.city = c
        sign.save()
        pro.f_name = f_name
        pro.m_name = m_name
        pro.hobby = ho
        pro.qualification = quali
        pro.work_address = w_add
        pro.f_contact = f_contact
        pro.f_contact = f_contact
        pro.salary = sal
        pro.occupation = occup
        pro.family_type = family
        cas1 = Religion.objects.get(religion=cas)
        pro.religion = cas1
        pro.save()
        error = True
    d = {'pro':pro,'religion':religion,'error':error}
    return render(request,'update_profile.html',d)


def Change_Password(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    error = ""
    if request.method=="POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        o = request.POST['pwd3']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            error = "yes"
        else:
            error = "not"
    d = {'error':error}
    return render(request,'change_password.html',d)

def Edit_status(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    sign = Signup.objects.get(id=pid)
    stat = Status.objects.all()
    if request.method == "POST":
        n = request.POST['username']
        s = request.POST['status']
        user = User.objects.get(username=n)
        sign.user.username = user
        status = Status.objects.get(status=s)
        sign.status = status
        sign.save()
        return redirect('requested_user')
    d = {'book': sign, 'stat': stat}
    return render(request, 'status.html', d)

def Edit_Caste(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    error = False
    religion = Religion.objects.get(id=pid)
    if request.method == "POST":
        c = request.POST['religion']
        religion.religion = c
        religion.save()
        error = True
    d = {'religion': religion,'error':error}
    return render(request, 'edit_religion.html', d)

def delete_religion(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    religion = Religion.objects.get(id=pid)
    religion.delete()
    return redirect('view_religion')

def delete_user(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    religion = User.objects.get(id=pid)
    religion.delete()
    return redirect('view_user')

def delete_feedback(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    feed = Send_Feedback.objects.get(id=pid)
    feed.delete()
    return redirect('view_feedback')

def Feedback(request, pid):
    if not request.user.is_authenticated:
        return redirect('login_user')
    error = False
    pro=""
    date1 = datetime.date.today()
    user = User.objects.get(id=pid)
    sign = Signup.objects.get(user=user)
    if request.method == "POST":
        d = request.POST['date']
        u = request.POST['uname']
        e = request.POST['email']
        con = request.POST['contact']
        m = request.POST['desc']
        user = User.objects.filter(username=u, email=e).first()
        pro = Signup.objects.filter(user=user, contact=con).first()
        Send_Feedback.objects.create(signup=pro, date=d, message1=m)
        error = True
    d = {'pro': sign, 'date1': date1,'error':error}
    return render(request, 'feedback.html', d)

def View_feedback(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    feed = Send_Feedback.objects.all()
    d = {'feed': feed}
    return render(request, 'view_feedback.html', d)


