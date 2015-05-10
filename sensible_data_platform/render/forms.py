from django import forms


class ChildNotificationForm(forms.Form):
    child_email = forms.CharField(label='child_email', max_length=100)
    child_questionnaire_url = forms.CharField(label='child_questionnaire_link', max_length=200)