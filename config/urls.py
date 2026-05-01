# from django.contrib import admin
# from django.urls import path, include
# from django.conf import settings
# from django.conf.urls.static import static
# from django.shortcuts import redirect

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', lambda r: redirect('dashboard'), name='root'),
#     path('accounts/', include('accounts.urls')),
#     path('dashboard/', include('timetables.urls')),
#     path('faculty/', include('faculty.urls')),
#     path('resources/', include('resources.urls')),
#     path('chatbot/', include('chatbot.urls')),
#     path('reports/', include('reports.urls')),
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# ============================================================
# config/urls.py  — REPLACE ENTIRELY
# ============================================================
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [

    path('',          lambda r: redirect('dashboard'), name='root'),
    path('admin/',    admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('dashboard/',  include('dashboard.urls')),
    path('timetables/', include('timetables.urls')),
    path('faculty/',    include('faculty.urls')),
    path('resources/',  include('resources.urls')),
    path('chatbot/',    include('chatbot.urls')),
    path('reports/',    include('reports.urls')),
    path('billing/',    include('billing.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)