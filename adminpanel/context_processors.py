from accounts.models import User
from wallet.models import Transaction

def admin_counts(request):
    if request.user.is_authenticated and request.user.is_staff:
        return {
            'pending_users': User.objects.filter(account_status='pending', account_opened=True).count(),
            'pending_deposits': Transaction.objects.filter(type='deposit', status='pending').count(),
            'pending_withdrawals': Transaction.objects.filter(type='withdraw', status='pending').count(),
        }
    return {}
