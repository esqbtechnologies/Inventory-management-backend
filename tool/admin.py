from django.contrib import admin
from .models.Usermodels import User
from .models.Assetmodels import asset
from .models.Verificationmodels import verification
from .models.Sessionmodels import session
from .models.Otpmodels import otp
from .models.Locationmodels import location
# Register your models here.
admin.site.register(User)
admin.site.register(asset)
admin.site.register(verification)
admin.site.register(session)
admin.site.register(otp)
admin.site.register(location)
