from django.db import models

# Create your models here.

class RSGEData(models.Model):
    index = models.AutoField(primary_key=True)
    reference = models.CharField()
    intitule = models.CharField()
    rubrique = models.CharField()
    chapitre = models.CharField()
    intitule_chapitre = models.CharField()
    intitule_rubrique = models.CharField()
    rubrique_complet = models.CharField()
    chapitre_complet = models.CharField()
    acronym = models.CharField()
    rubrique_affair_count = models.IntegerField()
    chapitre_affair_count = models.IntegerField()
    class Meta:
        managed=False
        db_table='data_rsge'

class RSGEVotingsData(models.Model):
    index = models.AutoField(primary_key=True)
    voting_id = models.CharField()
    voting_external_id = models.CharField()
    voting_date = models.CharField()
    voting_affair_external_id = models.CharField()
    voting_affair_number = models.CharField()
    voting_title_fr = models.CharField()
    voting_url_fr = models.CharField()
    voting_results_yes = models.CharField() 
    voting_results_no = models.CharField()
    voting_results_abstention = models.CharField() 
    voting_affair_title_fr = models.CharField() 
    reference = models.CharField()
    type_vote_label = models.CharField() 
    intitule = models.CharField() 
    date_d_adoption = models.CharField() 
    rubrique = models.CharField()
    chapitre = models.CharField() 
    intitule_rubrique = models.CharField() 
    intitule_chapitre = models.CharField() 
    rubrique_complet = models.CharField()
    chapitre_complet = models.CharField()
    acronym = models.CharField() 
    debat_numero = models.SmallIntegerField()
    initial_affair = models.CharField()

    class Meta:
        managed=False
        db_table='data_votings_rsge'

class otherVotingsData(models.Model):
    index = models.AutoField(primary_key=True)
    voting_id = models.CharField()
    voting_external_id = models.CharField()
    voting_date = models.CharField()
    voting_affair_external_id = models.CharField()
    voting_affair_number = models.CharField()
    voting_title_fr = models.CharField()
    voting_url_fr = models.CharField()
    voting_results_yes = models.CharField() 
    voting_results_no = models.CharField()
    voting_results_abstention = models.CharField() 
    voting_affair_title_fr = models.CharField() 
    type_vote_label = models.CharField() 
    class Meta:
        managed=False
        db_table='data_votings_others'


class votesData(models.Model):
    index = models.AutoField(primary_key=True)
    vote_external_id = models.CharField()
    vote_person_external_id = models.CharField()
    vote_person_fullname = models.CharField()
    vote_voting_external_id = models.CharField()
    vote_label = models.CharField()
    vote_vote_display_fr = models.CharField()
    class Meta:
        managed=False
        db_table='data_votes'

class personsData(models.Model):
    index = models.AutoField(primary_key=True)
    person_external_id = models.CharField()
    person_fullname = models.CharField()
    person_firstname = models.CharField()
    person_lastname = models.CharField()
    person_party_fr = models.CharField()
    person_website_parliament_url_fr = models.CharField()
    person_image_url = models.CharField()
    person_birthday =  models.CharField()
    person_occupation_fr = models.CharField()
    person_gender = models.CharField()
    person_function_latest_fr = models.CharField()
    class Meta:
        managed=False
        db_table='data_persons'