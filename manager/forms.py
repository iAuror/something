from django.forms import ModelForm, Textarea, TextInput, CharField, PasswordInput
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm
from manager.models import Comment, Books


class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(widget=TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    password = CharField(
        label=("Password"),
        strip=False,
        widget=PasswordInput(attrs={'autocomplete': 'current-password'}),
    )

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        pass
    username=UsernameField(widget=TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    password1 = CharField(
        label=("Password"),
        strip=False,
        widget=PasswordInput(attrs={'autocomplete': 'new-password','class': 'form-control'}),

    )
    password2 = CharField(
        label=("Password confirmation"),
        widget=PasswordInput(attrs={'autocomplete': 'new-password','class': 'form-control'}),
        strip=False,
        help_text=("Enter the same password as before, for verification."),
    )


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text', ]
        widgets = {
            'text': Textarea(attrs={'class': 'form-control',
                                    'rows': 3,
                                    }),
        }
        help_texts = {
            'text': '<bold> Тут можно написать какой то текст помощи'
        }


class BooksForm(ModelForm):
    class Meta:
        model = Books
        fields = ['title', 'text', 'shop', 'genre']
        widgets = {
            'text': Textarea(attrs={'class': 'form-control',
                                    'rows': 3,
                                    }),
            'title': TextInput(attrs={'class': 'form-control'}),

        }
