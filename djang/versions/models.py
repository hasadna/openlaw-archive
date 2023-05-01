from django.db import models


class Law(models.Model):
    # implicit ID
    wiki_page_id = models.IntegerField(unique=True)
    knesset_id = models.IntegerField(unique=True, null=True)
    akn_id = models.IntegerField(unique=True, null=True)
    name = models.CharField(max_length=50)
    # revisions: Can be calculated


class Revision(models.Model):
    # implicit ID
    law = models.ForeignKey(Law, on_delete=models.CASCADE)
    wiki_rev_id = models.IntegerField(unique=True)
    akn_id = models.IntegerField(
        unique=True, null=True
    )  # TODO do we need these both here and above?
    name = models.CharField(max_length=51)
    effective_date_start = models.DateField(null=True)
    effective_date_end = models.DateField(null=True)
    # source_text - will do later

