from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from .models import Law, Revision
from .forms import CompareForm
from .services.diff import diff

# Create your views here.


class LawChooseView(TemplateView):
    template_name = "versions/law_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        laws = Law.objects.all()
        context.update({"laws": laws})
        return context


class VersionCompareView(FormView):
    template_name = "versions/version_compare.html"
    form_class = CompareForm

    def get_context_data(self, **kwargs):
        ret = super().get_context_data(**kwargs)
        form = self.get_form()

        if form.law:
            ret["law"] = form.law

        if form.is_valid():
            ret["output"] = diff(
                revision_a=form.cleaned_data["version_a"],
                revision_b=form.cleaned_data["version_b"],
                style=form.cleaned_data["comparison_style"],
            )
        else:
            ret["output"] = ""
        return ret

    def get_form_kwargs(self):
        ret = super().get_form_kwargs()

        ret["data"] = self.request.GET

        pk = self.kwargs.get("pk")
        law = Law.objects.get(pk=pk)
        ret["law"] = law

        return ret

