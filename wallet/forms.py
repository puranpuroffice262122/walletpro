from django import forms
from .models import Transaction

class DepositForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'screenshot']
        widgets = {
            'amount': forms.NumberInput(attrs={'placeholder': 'Enter amount', 'min': '1', 'step': '0.01'}),
        }

class WithdrawForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'upi_id']
        widgets = {
            'amount': forms.NumberInput(attrs={'placeholder': 'Enter amount', 'min': '1', 'step': '0.01'}),
            'upi_id': forms.TextInput(attrs={'placeholder': 'yourname@upi'}),
        }
