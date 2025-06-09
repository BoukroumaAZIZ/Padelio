from django.contrib import admin

from reservation_app.models import Centre, Reservation, Terrain, User

admin.site.register(User)
admin.site.register(Terrain)
admin.site.register(Centre)
admin.site.register(Reservation)