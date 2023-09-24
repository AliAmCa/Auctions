from django import forms
from .models import Category
categories = []
result = Category.objects.all()
for item in result:
    categories.append((item.pk , item.name))

class NewProductForm(forms.Form):
    title = forms.CharField(label= 'Title',widget=forms.TextInput(attrs={'name':'title', 'class':'form-control'}))
    description = forms.CharField(label= 'Description',max_length=200, widget=forms.Textarea(attrs={'name':'description', 'rows':3, 'cols':5, 'class':'form-control'}))
    initialPrice = forms.FloatField(label='Initial Bid', min_value=0)
    image = forms.URLField(label='Image', required=False)
    category = forms.ChoiceField(label='Category', choices = categories, required=False)

    initialPrice.widget.attrs.update({'class':'form-control'})
    image.widget.attrs.update({'class':'form-control'})
    category.widget.attrs.update({'class':'form-control'})