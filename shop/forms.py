# shop/forms.py
from django import forms
from .models import Comment

class AddToCartForm(forms.Form):
    quantity = forms.ChoiceField(
        choices=[(str(i), str(i)) for i in range(1, 10)],  # Opciones del 1 al 9
        initial='1',
        label="Cantidad",
        widget=forms.Select(attrs={
            'class': 'form-control', 
            'style': 'width: 100px;'
        })
    )
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Escribe tu comentario...'}),
        }
