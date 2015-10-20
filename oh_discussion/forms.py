from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from . import models


class TopicCreateForm(forms.ModelForm):
    class Meta:
        model = models.OTopic
        fields = ['title', 'node', 'content']

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_method = 'POST'
        helper.add_input(Submit('submit', '发布'))
        return helper


class TopicUpdateForm(forms.ModelForm):
    class Meta:
        model = models.OTopic
        fields = ['title', 'node', 'content']

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_method = 'POST'
        helper.add_input(Submit('submit', '修改'))
        return helper
