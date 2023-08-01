from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, generics, permissions
import device_apis.serializers as api_serializers
from device_apis.models import Devices, DeviceSold, User
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import authenticate


# Create your views here.

@api_view(["GET"])
def home(request):
    message = {"message": "Hello, world"}
    return Response(message, status=200)


@api_view(["GET", "DELETE", "PUT"])
def list_devices(request):
    devices = [{"id": 1, "name": "MI 1", },
               {"id": 2, "name": "MI 2", },
               {"id": 3, "name": "Iphone 13", },
               {"id": 4, "name": "MI 4"}]
    return Response(devices, status=200)


class DeviceCreateView(generics.GenericAPIView):
    """
    This API is used to create a device, upon valid request the device will be created
    and a success message will be returned with device ID
    """
    serializer_class = api_serializers.DeviceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        print("request.data", self.request.data)
        device_data = self.serializer_class(data=self.request.data)
        if device_data.is_valid(raise_exception=True):
            device = device_data.create(validated_data=device_data.validated_data)
            return Response({"deviceId": device.id,
                             "message": "Device created successfully"},
                            status=status.HTTP_200_OK)
        return Response({"message": "Invalid request"},
                        status=status.HTTP_400_BAD_REQUEST)


class UserRegister(generics.GenericAPIView):
    """
    This API is used to register a user,
    upon valid request the user will be created
    and a success message will be returned with user ID
    """
    serializer_class = api_serializers.UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        print("request.data", self.request.data)
        check_valid_data = self.serializer_class(data=self.request.data)
        if check_valid_data.is_valid(raise_exception=True):
            user = check_valid_data.create(validated_data=check_valid_data.validated_data)
            return Response({"userId": user.id,
                             "message": "User created successfully"}, status=status.HTTP_200_OK)
        return Response({"message": "Invalid request",
                         "error": self.serializer_class.errors}, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(generics.GenericAPIView):
    """
    This API is used to create a JWT token for APIs which require authentication
    """
    serializer_class = api_serializers.UserLoginTokenSerializer

    def post(self, request, *args, **kwargs):
        print("request.data", self.request.data)
        check_valid_request = self.serializer_class(data=self.request.data)
        if check_valid_request.is_valid(raise_exception=True):
            user = authenticate(username=check_valid_request.validated_data['username'],
                                password=check_valid_request.validated_data['password'])
            if user:
                token = AccessToken.for_user(user)
                return Response({"userId": user.id, "token": str(token)}, status=status.HTTP_200_OK)
        return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


class DeviceListView(generics.GenericAPIView):
    """
    This API is used to list all the devices
    """
    serializer_class = api_serializers.DeviceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        print("request.data", self.request.data)
        self.queryset = Devices.objects.all()
        return Response(self.serializer_class(self.queryset, many=True).data,
                        status=status.HTTP_200_OK)


class DeviceDetailView(generics.GenericAPIView):
    """
    This API is used to get the detail of a single device
    """
    serializer_class = api_serializers.DeviceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, device_id, *args, **kwargs):
        try:
            device = Devices.objects.get(id=device_id)
            return Response(self.serializer_class(device).data,
                            status=status.HTTP_200_OK)
        except Devices.DoesNotExist as e:
            return Response({"message": "Device not found",
                             "error": str(e.__class__.__name__)},
                            status=status.HTTP_404_NOT_FOUND)

