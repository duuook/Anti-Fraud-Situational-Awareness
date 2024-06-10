from django import forms
from SE import models


class PhoneNumberModelForm(forms.ModelForm):
    """电话号码表表单"""

    class Meta:
        model = models.phone_number
        fields = ['id', '电话号码', '电话类型', '标记次数']

    def __init__(self, *args, **kwargs):
        super(PhoneNumberModelForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'style': 'text-align:center'}


class msgModelForm(forms.ModelForm):
    """短信表表单"""

    class Meta:
        model = models.msg
        fields = ['id', '短信类别', '短信内容']

    def __init__(self, *args, **kwargs):
        super(msgModelForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control'}


class WebsiteModelForm(forms.ModelForm):
    """网站表表单"""

    class Meta:
        model = models.website
        fields = ['id', '网站域名', '诈骗类型']

    def __init__(self, *args, **kwargs):
        super(WebsiteModelForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control'}
