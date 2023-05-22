from django.db import models
from datetime import date


class Law(models.Model):
    # implicit ID
    wiki_page_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=250)


class Revision(models.Model):
    # implicit ID
    law = models.ForeignKey(Law, on_delete=models.CASCADE)
    wiki_rev_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=251)
    effective_date_start = models.DateField(null=True)
    source_text = models.TextField()

    @classmethod
    def get_by_law_and_epoch(cls, law, epoch):
        d = date.fromtimestamp(epoch)
        return (
            law.revision_set.filter(effective_date_start__lte=d)
            .order_by("-effective_date_start")
            .first()
        )
