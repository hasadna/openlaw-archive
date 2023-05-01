from django import forms
from .models import Law, Revision


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
