from django import forms
from .models import MyBizprocModel


class MyBPForm(forms.ModelForm):
    class Meta:
        model = MyBizprocModel
        fields = []

    bp = forms.ModelChoiceField(
        queryset=MyBizprocModel.objects.all(),
        to_field_name='process_id',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label='Не выбрано',
        label='БП'
    )
