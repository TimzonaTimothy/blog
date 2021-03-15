from django import forms
from main.models import Post,Comment,Category,Subscribe
from ckeditor.fields import RichTextField

cats = Category.objects.all().values_list('name','name')
cats_list = []

for item in cats:
    cats_list.append(item)

class PostForm(forms.ModelForm):
    text = content = RichTextField()
    class Meta():
        model = Post
        fields = ('image','category','title','text',)

        widgets = {
            'title':forms.TextInput(attrs={'class':'textinputclass'}),
            # 'author':forms.TextInput(attrs={'class':'form-control'}),
            'category':forms.Select(choices=cats_list,attrs={'class':'form-control'}),
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})
        }




class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        fields = ('name','text',)

        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'text':forms.Textarea(attrs={'class':'form-control'}),
        }


class SubscribeForm(forms.ModelForm):
    class Meta():
        model = Subscribe
        fields = ('email',)
        widgets = {
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Your email'}),
        }