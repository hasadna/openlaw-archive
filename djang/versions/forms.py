from django import forms
from .models import Law, Revision


class SliderWidget(forms.Widget):
    template_name = "versions/slider.html"

    def __init__(self):
        super().__init__()
        self.disabled = True

    def get_context(self, name, value, attrs):
        ret = super().get_context(name, value, attrs)
        if not self.disabled:
            ret["widget"]["steps"] = self.steps
            ret["widget"]["min"] = self.min
            ret["widget"]["max"] = self.max
        return ret

    def set_law(self, law):
        self.law = law
        revisions = law.revision_set.filter(effective_date_start__isnull=False)
        if not revisions.exists():
            self.disabled = True
            return

        self.disabled = False

        revisions = revisions.order_by("effective_date_start").values(
            "effective_date_start"
        )
        dates = [r["effective_date_start"] for r in revisions]
        earliest = dates[0]
        latest = dates[-1]
        steps = dates

        self.min = earliest.strftime("%s")
        self.max = latest.strftime("%s")
        self.steps = [{"value": s.strftime("%s"), "label": s} for s in steps]


class RevisionModelChoiceField(forms.ModelChoiceField):
    def __init__(self, *args, **kwargs):
        kwargs["queryset"] = None
        kwargs["empty_label"] = None
        super().__init__(*args, **kwargs)
        pass

    def set_law(self, law):
        self.queryset = law.revision_set.all()

    def label_from_instance(self, obj):
        return obj.name


class CompareForm(forms.Form):
    version_a = RevisionModelChoiceField()
    version_b = RevisionModelChoiceField()
    # TODO move to somewhere else
    comparison_style = forms.ChoiceField(
        choices=[
            ("basic", "basic"),
            ("law", "law"),
            ("wiki", "wiki"),
            ("html", "html"),
        ]
    )

    def get_choices(self):
        return self.law.revision_set.all()

    def __init__(self, law, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.law = law
        self.fields["version_a"].set_law(law)
        self.fields["version_b"].set_law(law)


class TimelineForm(forms.Form):
    timey = forms.IntegerField(widget=SliderWidget())

    def __init__(self, law, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.law = law
        self.fields["timey"].widget.set_law(law)
