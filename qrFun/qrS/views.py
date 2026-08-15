from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout,get_user_model
from .models import Qrcode
import qrcode
from django.conf import settings
from django.core.files.base import ContentFile
import io

User = get_user_model()


def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Email already registered'})

        user = User.objects.create_user(email=email, password=password)
        login(request, user)
        return redirect('gallery')

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('gallery')
        return render(request, 'login.html', {'error': 'Invalid email or password'})

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def upload_view(request):
    if request.method == 'POST':
        label = request.POST.get('label', 'Scan for Menu')
        file = request.FILES.get('file')

        content_type = file.content_type  # e.g. 'image/png' or 'video/mp4'
        media_type = 'video' if content_type.startswith('video') else 'image'

        item = Qrcode.objects.create(user=request.user, label=label, file=file, media_type=media_type)

        scan_url = f"{settings.SITE_URL}/scan/{item.id}/"
        qr = qrcode.QRCode(box_size=10, border=4)
        qr.add_data(scan_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        item.qr_code.save(f"{item.id}.png", ContentFile(buffer.getvalue()), save=True)

        return redirect('gallery')

    return render(request, 'upload.html')


@login_required
def gallery_view(request):
    items = Qrcode.objects.filter(user=request.user)
    return render(request, 'gallery.html', {'items': items})


def scan_view(request, pk):
    item = get_object_or_404(Qrcode, pk=pk)
    return render(request, 'scan.html', {'item': item})