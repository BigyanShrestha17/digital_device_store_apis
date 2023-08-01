
from django.contrib import admin
from django.urls import path
import device_apis.views as api_views

urlpatterns = [
    path("api/get-token", api_views.UserLogin.as_view(), name="get_auth_token"),
    # path("", api_views.home, name="home"),
    # path("api/devices", api_views.list_devices, name="list_devices"),
    path("api/create-device", api_views.DeviceCreateView.as_view(), name="create_device"),
    path("api/register", api_views.UserRegister.as_view(), name="user_register"),
    path("api/get-devices", api_views.DeviceListView.as_view(), name="list_device"),
    path("api/device-detail/<int:device_id>",
         api_views.DeviceDetailView.as_view(), name="device_detail"),
]