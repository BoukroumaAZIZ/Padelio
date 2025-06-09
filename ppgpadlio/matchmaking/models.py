from django.db import models
from reservation_app.models import User

class Match(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matches_faits')
    cible = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matches_recus')
    liked = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('utilisateur', 'cible')


