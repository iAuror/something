from django.forms import ModelForm, Textarea

from manager.models import Comment


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text', ]
        widgets = {
            'text': Textarea(attrs={'class': 'form-control',
                                    'rows':3,
                                    }),
        }
        help_texts={
            'text':'<bold> Тут можно написать какой то текст помощи'
        }
