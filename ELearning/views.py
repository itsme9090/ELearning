from django.shortcuts import render,HttpResponse,redirect

# Create your views here.
from .models import *
from django.contrib.auth.hashers import check_password,make_password
from Tutorial_Tech.settings import *
import razorpay
from time import time
from django.views.decorators.csrf import csrf_exempt

client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))

def home(request):
    course_dtls=Course_details.objects.all()
    context={
        'course_dtls':course_dtls,
    
    }
    return render(request,'index.html',context=context)

def contact(request):
    return render(request,'contact.html')

def sign_up(request):
    if request.method=='POST':
        f_name=request.POST.get('fname')
        l_name=request.POST.get('lname')
        email_id=request.POST.get('email')
        password=request.POST.get('password')
        gender=request.POST.get('gender')
        mobile=request.POST.get('mobile')

        sign_obj=Signup(
            first_name=f_name,
            last_name=l_name,
            email=email_id,
            password=make_password(password),
            gender=gender,
            mobile=mobile,
        )
        sign_obj.save()
        return HttpResponse("Registration successful")

def login(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')

        # email_id=Signup.objects.filter(email=email)
        try:
            email_id=Signup.objects.get(email=email)

            if email_id:
                if check_password(password,email_id.password):
                    # return HttpResponse("Login Successful")
                    request.session['name']=email_id.first_name
                    request.session['email']=email_id.email
                    return redirect('home')
                else:
                    return HttpResponse("Wrong password")
                # return HttpResponse("email exists")
        # else:
        except:
            return HttpResponse("email not found")
        

def logout(request):
    request.session.clear()
    return redirect('home')


def course(request,slug):
    course=Course_details.objects.get(slug=slug)
    s_no=request.GET.get('serial_no')

    if s_no is None:
        s_no=1
    try:
        video=Videos.objects.get(video_belong=course,video_seq=s_no)
        if video.is_preview is False:
            if request.session.get('name') is None:
                return redirect('home')
            else:
                user_id= Signup.objects.get(email=request.session['email'])
                # print(user_id)
                # try:
                #     user_course=userCourse.objects.get(
                #         user=user_id,course=fetch_dtls)
                # except:
                #     return redirect('checkout',slug=fetch_dtls.slug)
    except:
        return redirect('home')
    return render(request,'course.html',{'video_fetch':course,'video':video})
    # video_fetch=Videos.objects.filter(video_belong=1)
    # print(slug)
    # return render(request,'course.html',{'video_fetch':video_fetch})


def checkout(request,slug):
    course=Course_details.objects.get(slug=slug)
    coupon_code=request.GET.get('coupon')

    try:
        user_id=Signup.objects.get(email=request.session['email'])
    except:
        return redirect('home')

    payment=None
    order=None
    order_id=None
    error=None
    cpn_code_msg=None
    coup=None
    amount=None
    if error is None:
    # if amount is None:
    #     amount=1
    # else:
        amount=int((course.price-(course.price*course.discount*0.01))*100)   
        # tp=int(amount*100)
    # print('---------',tp)
    # if coup:
    if coupon_code:
        try:
            coup=Ref_code.objects.get(course=course,code=coupon_code)
            amount=int((course.price-(course.price*coup.discount*0.01))*100)
            # tp=int(amount*100)
            # coup_msg="coupan applied successfully"
            
        except:
            cpn_code_msg='Invalid Coupon Code'

    create_payment=request.GET.get('action')
    if create_payment=='payment':
        try:
            user_course=User_Course.objects.get(user=user_id,course=course)
            return HttpResponse('you have already purchased this course')
        except:
            pass
        
        # pay=1
        data = { "amount": amount, "currency": "INR", "receipt": f"tutorial_tech-{int(time())}" }
        order= client.order.create(data=data)

        order_id=order.get('id')
        payment=Payment()
        payment.order_id=order_id
        payment.course=course
        payment.user_info=user_id
        payment.save()


    context={
        'course':course,
        'pay':1,
        'order':order,
        'order_id':order_id,
        'amount':amount,
        'coupon_msg':cpn_code_msg,
        'coup':coup
    }
    return render(request,'checkout.html',context=context)


@csrf_exempt
def verify_payment(request):
    if request.method=='POST':
        # print(request.POST)
        data=request.POST
        # print(data)
        client.utility.verify_payment_signature(
            data
        # 'razorpay_order_id': razorpay_order_id,
        # 'razorpay_payment_id': razorpay_payment_id,
        # 'razorpay_signature': razorpay_signature
        )
        payment=Payment.objects.get(order_id=data['razorpay_order_id'])
        payment.payment_id=data['razorpay_payment_id']
        payment.status=True

        # payment.save()

        usercourse=User_Course(user=payment.user_info,course=payment.course)
        usercourse.save()

        payment.course_info=usercourse
        payment.save()
    
    try:
        return redirect('home')
    except:
        return HttpResponse('not working')



def blog(request):
    return render(request,'blog.html')




def mycourse(request):
    user_id=Signup.objects.get(email=request.session['email'])
    user_course=User_Course.objects.filter(user=user_id)
    context={
        'user_course':user_course
    }

    return render(request,'mycourse.html',context=context)


from .Serializers import *
from rest_framework import viewsets


class UserViewSet(viewsets.ModelViewSet):
    queryset = Signup.objects.all()
    serializer_class = SignUpSerializer



