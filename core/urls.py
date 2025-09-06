from django.contrib import admin
from django.urls import path , include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/',include('accounts.urls',namespace='accounts')),
    path('friend/',include('friends.urls',namespace='friends')),
    path('posts/',include('posts.urls',namespace='posts'))
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
