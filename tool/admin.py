from django.contrib import admin
from .models.Usermodels import User
from .models.Assetmodels import asset
from .models.Verificationmodels import verification
from .models.Sessionmodels import session
# Register your models here.
admin.site.register(User)
admin.site.register(asset)
admin.site.register(verification)
admin.site.register(session)
