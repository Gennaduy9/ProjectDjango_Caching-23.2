from django import forms

from catalog.models import Product, Version


class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Product
        exclude = ('owner',)

    def clean_name(self):
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар']
        cleaned_data = self.cleaned_data['name']
        for i in range(len(forbidden_words)):
            if cleaned_data.lower() == forbidden_words[i]:
                raise forms.ValidationError('Запрещенный продукт')
        return cleaned_data

    def clean_description(self):
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар']
        cleaned_data = self.cleaned_data['description']
        for i in range(len(forbidden_words)):
            if forbidden_words[i] in cleaned_data.lower():
                raise forms.ValidationError('Запрещенное описание продукта')
        return cleaned_data


class VersionForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Version
        fields = '__all__'


class ProductCuttedForm(StyleFormMixin, forms.ModelForm):
    name = forms.CharField(max_length=100, disabled=True)
    photo = forms.ImageField(disabled=True)
    price = forms.IntegerField(disabled=True)

    class Meta:
        model = Product
        exclude = ('owner',)
