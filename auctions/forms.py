from django import forms

categories = [('1','Fashion'), ('2','Toys'), ('3','Electronics'), ('4','Home'),('5', 'Sport')]
class NewProductForm(forms.Form):
    title = forms.CharField(label= 'Title',widget=forms.TextInput(attrs={'name':'title', 'class':'form-control'}))
    description = forms.CharField(label= 'Description', widget=forms.Textarea(attrs={'name':'description', 'rows':3, 'cols':5, 'class':'form-control'}))
    initialPrice = forms.FloatField(label='Initial Bid')
    image = forms.URLField(label='Image')
    category = forms.ChoiceField(label='Category', choices = categories, required=False)

    initialPrice.widget.attrs.update({'class':'form-control'})
    image.widget.attrs.update({'class':'form-control'})
    category.widget.attrs.update({'class':'form-control'})