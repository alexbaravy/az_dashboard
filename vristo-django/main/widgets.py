from django.forms.widgets import TextInput


class CustomTextInput(TextInput):
    def __init__(self, *args, **kwargs):
        attrs = kwargs.get('attrs', {})
        attrs.update({
            'placeholder': 'Username',
            'class': 'form-input ltr:rounded-l-none rtl:rounded-r-none py-2.5 text-base',
        })
        kwargs['attrs'] = attrs
        super().__init__(*args, **kwargs)
