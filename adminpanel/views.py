from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from accounts.models import User
from wallet.models import Transaction, Notification, Product, Order, Advertisement

def admin_required(view_func):
    return staff_member_required(view_func, login_url='/accounts/login/')

@admin_required
def dashboard(request):
    total_users = User.objects.filter(is_staff=False).count()
    active_users = User.objects.filter(account_status='active').count()
    pending_users = User.objects.filter(account_status='pending', account_opened=True).count()
    pending_deposits = Transaction.objects.filter(type='deposit', status='pending').count()
    pending_withdrawals = Transaction.objects.filter(type='withdraw', status='pending').count()
    total_balance = User.objects.aggregate(t=Sum('balance'))['t'] or 0
    total_deposits = Transaction.objects.filter(type='deposit', status='approved').aggregate(t=Sum('amount'))['t'] or 0
    total_withdrawals = Transaction.objects.filter(type='withdraw', status='approved').aggregate(t=Sum('amount'))['t'] or 0
    recent_users = User.objects.filter(account_status='pending', account_opened=True).order_by('-created_at')[:5]
    recent_txns = Transaction.objects.select_related('user').filter(status='pending').order_by('-created_at')[:6]
    context = {
        'total_users': total_users, 'active_users': active_users,
        'pending_users': pending_users, 'pending_deposits': pending_deposits,
        'pending_withdrawals': pending_withdrawals, 'total_balance': total_balance,
        'total_deposits': total_deposits, 'total_withdrawals': total_withdrawals,
        'recent_users': recent_users, 'recent_txns': recent_txns,
    }
    return render(request, 'adminpanel/dashboard.html', context)

@admin_required
def users(request):
    status = request.GET.get('status', '')
    search = request.GET.get('q', '')
    qs = User.objects.filter(is_staff=False)
    if status:
        qs = qs.filter(account_status=status)
    if search:
        qs = qs.filter(Q(email__icontains=search)|Q(first_name__icontains=search)|Q(last_name__icontains=search))
    return render(request, 'adminpanel/users.html', {'users': qs, 'filter': status, 'search': search})

@admin_required
def user_action(request, pk):
    user = get_object_or_404(User, pk=pk)
    action = request.POST.get('action')
    note = request.POST.get('admin_note', '')
    if action == 'approve':
        user.account_status = 'active'
        user.admin_note = note
        if not user.account_number:
            from accounts.models import generate_account_number
            user.account_number = generate_account_number()
        user.save()
        Notification.objects.create(user=user, message='Your account has been approved! You can now deposit and withdraw.')
        messages.success(request, f'{user.get_full_name()} approved.')
    elif action == 'reject':
        user.account_status = 'rejected'
        user.admin_note = note
        user.save()
        Notification.objects.create(user=user, message=f'Your account was rejected. Reason: {note}')
        messages.warning(request, f'{user.get_full_name()} rejected.')
    elif action == 'suspend':
        user.account_status = 'suspended'
        user.save()
        messages.warning(request, f'{user.get_full_name()} suspended.')
    elif action == 'activate':
        user.account_status = 'active'
        user.save()
        messages.success(request, f'{user.get_full_name()} activated.')
    elif action == 'delete':
        user.delete()
        messages.error(request, 'User deleted.')
    elif action == 'edit':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.upi_id = request.POST.get('upi_id', user.upi_id)
        bal = request.POST.get('balance')
        if bal:
            user.balance = bal
        user.save()
        messages.success(request, 'User updated.')
    return redirect('adminpanel:users')

@admin_required
def deposits(request):
    status = request.GET.get('status', 'pending')
    txns = Transaction.objects.filter(type='deposit').select_related('user')
    if status:
        txns = txns.filter(status=status)
    return render(request, 'adminpanel/deposits.html', {'txns': txns, 'filter': status})

@admin_required
def deposit_action(request, pk):
    txn = get_object_or_404(Transaction, pk=pk, type='deposit')
    action = request.POST.get('action')
    note = request.POST.get('admin_note', '')
    if action == 'approve' and txn.status == 'pending':
        txn.status = 'approved'
        txn.admin_note = note
        txn.save()
        txn.user.balance += txn.amount
        txn.user.save()
        Notification.objects.create(user=txn.user, message=f'Deposit of ₹{txn.amount} approved! Balance updated.')
        messages.success(request, f'Deposit ₹{txn.amount} approved.')
    elif action == 'reject' and txn.status == 'pending':
        txn.status = 'rejected'
        txn.admin_note = note
        txn.save()
        Notification.objects.create(user=txn.user, message=f'Deposit of ₹{txn.amount} rejected. Reason: {note}')
        messages.warning(request, 'Deposit rejected.')
    return redirect('adminpanel:deposits')

@admin_required
def withdrawals(request):
    status = request.GET.get('status', 'pending')
    txns = Transaction.objects.filter(type='withdraw').select_related('user')
    if status:
        txns = txns.filter(status=status)
    return render(request, 'adminpanel/withdrawals.html', {'txns': txns, 'filter': status})

@admin_required
def withdrawal_action(request, pk):
    txn = get_object_or_404(Transaction, pk=pk, type='withdraw')
    action = request.POST.get('action')
    note = request.POST.get('admin_note', '')
    if action == 'approve' and txn.status == 'pending':
        if txn.user.balance >= txn.amount:
            txn.status = 'approved'
            txn.admin_note = note
            txn.save()
            txn.user.balance -= txn.amount
            txn.user.save()
            Notification.objects.create(user=txn.user, message=f'Withdrawal of ₹{txn.amount} approved!')
            messages.success(request, f'Withdrawal ₹{txn.amount} approved.')
        else:
            messages.error(request, 'Insufficient user balance.')
    elif action == 'reject' and txn.status == 'pending':
        txn.status = 'rejected'
        txn.admin_note = note
        txn.save()
        Notification.objects.create(user=txn.user, message=f'Withdrawal of ₹{txn.amount} rejected. Reason: {note}')
        messages.warning(request, 'Withdrawal rejected.')
    return redirect('adminpanel:withdrawals')

@admin_required
def all_transactions(request):
    txns = Transaction.objects.select_related('user').all()
    return render(request, 'adminpanel/transactions.html', {'txns': txns})

@admin_required
def products_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        desc = request.POST.get('description', '')
        cat = request.POST.get('category', 'General')
        img = request.FILES.get('image')
        Product.objects.create(name=name, price=price, description=desc, category=cat, image=img)
        messages.success(request, 'Product added.')
        return redirect('adminpanel:products')
    prods = Product.objects.all()
    return render(request, 'adminpanel/products.html', {'products': prods})

@admin_required
def toggle_product(request, pk):
    prod = get_object_or_404(Product, pk=pk)
    prod.is_active = not prod.is_active
    prod.save()
    return redirect('adminpanel:products')

@admin_required
def orders_view(request):
    orders = Order.objects.select_related('user', 'product').all()
    return render(request, 'adminpanel/orders.html', {'orders': orders})
