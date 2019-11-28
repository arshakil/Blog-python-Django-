from django import forms
from . models import Comment,Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('message',)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['message'].widget.attrs.update({'class':'form-control','rows':'5','cols':'30','placeholder':'Message'})



class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('category','title','image','description','tags')
        
    def __init__(self, *arg, **kwarg):
        super(PostCreateForm, self).__init__(*arg, **kwarg)
        
        self.fields["category"].widget.attrs.update({'class':'form-control','placeholder':'Select your category'})
        self.fields["title"].widget.attrs.update({'class':'form-control','placeholder':'Enter title'})
        self.fields["image"].widget.attrs.update({'class':'form-control',})
        self.fields["description"].widget.attrs.update({'class':'form-control','placeholder':'Enter Post Description'})
        self.fields["tags"].widget.attrs.update({'class':'form-control','placeholder':'tags must be separated by comma such as-->    fashion,dress '})
        
        