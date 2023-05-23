from django.core.management.base import BaseCommand, CommandError
from versions.services import wiki
from versions import models


def process_law(law_in: wiki.PageResult, force: bool):
    # Get law
    if not force and models.Law.objects.filter(wiki_page_id=law_in.page_id).exists():
        return
    law, law_created = models.Law.objects.get_or_create(
        wiki_page_id=law_in.page_id, defaults={"name": law_in.title}
    )
    law.save()
    # Revisions
    revisions_in = wiki.get_revisions_for_page(page_title=law_in.title)
    # TODO do the splits!
    for revision_in in revisions_in:
        models.Revision.objects.get_or_create(
            law=law,
            wiki_rev_id=revision_in.id,
            defaults={
                "name": revision_in.comment,
                "effective_date_start": revision_in.timestamp,
                "source_text": revision_in.content,
            },
        )

    # Get all revisions for said law
    # group by major revisions
    # how to identifiy major revision:
    # extract Makor: line with <מקור> until double newline
    # if Makor changed, this is a major revision
    # for each major revision, choose the latest non-major revision as source for text.
    # extract from the latest non-major revision the title from the Makor row
    # from the earliest revision in the major revision, get the edit date as the effective date
    pass


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--law-name", required=False)
        parser.add_argument("--force", action="store_true")

    def handle(self, *args, **options):
        force = options["force"]
        if law_name := options["law_name"]:
            page = wiki.get_page(law_name)
            process_law(page, force=force)
        else:
            for page in wiki.get_pages_in_category():
                print(page.title)
                process_law(page, force=force)
