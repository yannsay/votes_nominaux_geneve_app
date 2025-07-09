from django.db import models

# Create your models here.

class RSGEChapter(models.Model):
    index = models.AutoField(primary_key=True)
    reference = models.CharField()
    intitule = models.CharField()
    rubrique = models.CharField()
    chapitre = models.CharField()
    intitule_chapitre = models.CharField()
    intitule_rubrique = models.CharField()
    acronym = models.CharField()
    class Meta:
        managed=False
        db_table='RSGEChapter'