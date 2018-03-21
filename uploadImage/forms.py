from django import forms

class ImageForm(forms.Form):
   Title = forms.CharField(max_length = 30)
   Description = forms.CharField(max_length = 200)
   Category = forms.CharField(max_length=30)
   Tag = forms.IntegerField()
   ImageFile = forms.ImageField()