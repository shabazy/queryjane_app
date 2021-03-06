import json

from django.db import transaction
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import FormView
from django.views.generic import TemplateView
from django.views.generic.edit import DeleteView
from django.views.generic import View
from django.urls import reverse

from account.models import IndustryCategory
from app.mixins import CustomUserMixin
from entrepreneur.data import VENTURE_STATUS_ACTIVE
from entrepreneur.data import VENTURE_STATUS_INACTIVE
from entrepreneur.forms import CompanyLogoForm
from entrepreneur.forms import VentureDescriptionForm
from entrepreneur.models import Venture
from entrepreneur.permissions import EntrepreneurPermissions


class GeneralCompanyFormView(CustomUserMixin, TemplateView):
    template_name = 'entrepreneur/venture_settings/general_company_settings.html'

    def get_object(self):
        return get_object_or_404(
            Venture,
            slug=self.kwargs.get('slug'),
        )

    def test_func(self):
        return EntrepreneurPermissions.can_manage_company(
            user=self.request.user,
            company=self.get_object()
        )

    def get(self, *args, **kwargs):
        company = self.get_object()

        return self.render_to_response(
            self.get_context_data(
                company=company,
                company_logo_form=CompanyLogoForm(),
                description_form=VentureDescriptionForm(
                    initial={
                        'description_es': company.description_es,
                        'description_en': company.description_en,
                    },
                ),
                industry_categories=IndustryCategory.objects.all(),
                general_active=True,
                can_delete=EntrepreneurPermissions.can_delete_company(
                    user=self.request.user,
                    company=self.get_object()
                )
            )
        )


class UpdateCompanyLogoForm(CustomUserMixin, FormView):
    form_class = CompanyLogoForm

    def get_object(self):
        return get_object_or_404(
            Venture,
            slug=self.kwargs.get('slug'),
        )

    def test_func(self):
        return EntrepreneurPermissions.can_manage_company(
            user=self.request.user,
            company=self.get_object(),
        )

    def form_valid(self, form):
        company = self.get_object()
        company.logo = form.cleaned_data['logo']
        company.save()

        return JsonResponse({'content': company.get_logo})


class CompanyCategoryView(CustomUserMixin, View):
    def get_object(self):
        return get_object_or_404(
            Venture,
            slug=self.kwargs.get('slug')
        )

    def test_func(self):
        return EntrepreneurPermissions.can_manage_company(
            user=self.request.user,
            company=self.get_object()
        )

    @transaction.atomic
    def post(self, request, **kwargs):
        company = self.get_object()

        category_id = request.POST.get('category_id')
        new_status = request.POST.get('new_status')
        new_status = json.loads(new_status)

        category = get_object_or_404(
            IndustryCategory,
            id=category_id,
        )

        if (
            company.industry_categories.count() == 1 and
            not new_status
        ):
            return HttpResponse('minimum_error')

        if new_status:
            company.industry_categories.add(category)
        else:
            company.industry_categories.remove(category)
        company.save()

        return HttpResponse('success')


class UpdateVentureDescriptionForm(CustomUserMixin, FormView):
    form_class = VentureDescriptionForm

    def get_object(self):
        return get_object_or_404(Venture, slug=self.kwargs.get('slug'))

    def test_func(self):
        return EntrepreneurPermissions.can_manage_company(
            user=self.request.user,
            company=self.get_object()
        )

    def form_valid(self, form):
        venture = self.get_object()
        description_es = form.cleaned_data['description_es']
        description_en = form.cleaned_data['description_en']

        updated_es = False
        if venture.description_es != description_es:
            updated_es = True
            venture.description_es = description_es

        updated_en = False
        if venture.description_en != description_en:
            updated_en = True
            venture.description_en = description_en

        venture.save()

        return JsonResponse(
            {
                'content': {
                    'updated_es': updated_es,
                    'description_es': venture.description_es,
                    'updated_en': updated_en,
                    'description_en': venture.description_en,
                },
            },
        )


class DeactivateCompanyView(CustomUserMixin, View):
    """
    Ajax view to deactivate a company in the platform.
    All company's information will be diabled for all users,
    and will be available only for users with administrator
    membership in the company and for platform administrators.
    """
    def get_object(self):
        return get_object_or_404(
            Venture,
            slug=self.kwargs.get('slug')
        )

    def test_func(self):
        return EntrepreneurPermissions.can_manage_company(
            user=self.request.user,
            company=self.get_object()
        )

    @transaction.atomic
    def post(self, request, **kwargs):
        company = self.get_object()

        company.status = VENTURE_STATUS_INACTIVE
        company.save()

        return HttpResponse('success')


class ActivateCompanyView(CustomUserMixin, View):
    """
    Ajax view to activate a company in the platform.
    All company information will be available for all
    users.
    """
    def get_object(self):
        return get_object_or_404(
            Venture,
            slug=self.kwargs.get('slug')
        )

    def test_func(self):
        return EntrepreneurPermissions.can_manage_company(
            user=self.request.user,
            company=self.get_object()
        )

    @transaction.atomic
    def post(self, request, **kwargs):
        company = self.get_object()

        company.status = VENTURE_STATUS_ACTIVE
        company.save()

        return HttpResponse('success')


class DeleteCompanyView(CustomUserMixin, DeleteView):
    """
    Company delete view. Only company owner can delete a
    company. User will be redirected to a view in which
    he will be asked about confirmation for delete a company
    definitely. A list with job offers and memberships that
    will be delete is displayed too.
    """
    model = Venture
    template_name = 'entrepreneur/venture_settings/company_delete.html'

    def get_object(self):
        return get_object_or_404(
            Venture,
            slug=self.kwargs.get('slug')
        )

    def test_func(self):
        return EntrepreneurPermissions.can_delete_company(
            user=self.request.user,
            company=self.get_object()
        )

    def get_success_url(self):
        return reverse(
            'dashboard',
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = self.get_object()
        context['general_active'] = True

        return context
