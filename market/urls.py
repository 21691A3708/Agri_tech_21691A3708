from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('chat/',views.chat,name="chat"),
    path('chat/<int:chat_id>/', views.chat_room, name='chat_room'),
    #farmers
    path('farmer_home/', views.farmer_home, name='farmer_home'),
    path('fupdate_profile/', views.fupdate_profile, name='fupdate_profile'),
    path('farmer_productions/', views.farmer_productions, name='farmer_productions'),
    path('production/<int:pk>/', views.production_detail, name='production_detail'),
    path('production/<int:pk>/edit/', views.edit_production, name='edit_production'),
    path('production/<int:pk>/delete/', views.delete_production, name='delete_production'),
    path('add_production/', views.add_production, name='add_production'),
    path('fchange_password/', views.fchange_password, name='fchange_password'),
    path('buyers/', views.buyer_list, name='buyer_list'),


    path('buyer_profile/<str:username>/', views.buyer_profile, name='buyer_profile'),

    #buyers
    path('buyer_home/', views.buyer_home, name='buyer_home'),
    path('bupdate_profile/', views.bupdate_profile, name='bupdate_profile'),
    path('farmers_list/', views.farmers_list, name='farmers_list'),
    path('farmer_profile/<str:username>/', views.farmer_profile, name='farmer_profile'),
    path('bproduction_list/<str:username>/', views.bproduction_list, name='bproduction_list'),
    path('bproduction/<int:pk>/', views.bproduction_detail, name='bproduction_detail'),
    path('bchange_password/', views.bchange_password, name='bchange_password'),
    
    
    path('purchases/', views.purchases, name='purchases'),
    path('payment_history/', views.payment_history, name='payment_history'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

