from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Transaction, Notification, Product, Order
from .forms import DepositForm, WithdrawForm

@login_required
def dashboard(request):
    user = request.user
    recent_txns = user.transactions.all()[:5]
    unread_notifs = user.notifications.filter(is_read=False).count()
    products = Product.objects.filter(is_active=True)[:6]
    context = {
        'user': user,
        'recent_txns': recent_txns,
        'unread_notifs': unread_notifs,
        'products': products,
    }
    return render(request, 'wallet/dashboard.html', context)

@login_required
def deposit(request):
    if request.user.account_status != 'active':
        messages.warning(request, 'Your account must be active to make deposits.')
        return redirect('wallet:dashboard')
    if request.method == 'POST':
        form = DepositForm(request.POST, request.FILES)
        if form.is_valid():
            txn = form.save(commit=False)
            txn.user = request.user
            txn.type = 'deposit'
            txn.save()
            messages.success(request, 'Deposit request submitted! Admin will approve it shortly.')
            return redirect('wallet:transactions')
    else:
        form = DepositForm()
    return render(request, 'wallet/deposit.html', {'form': form})

@login_required
def withdraw(request):
    user = request.user
    if user.account_status != 'active':
        messages.warning(request, 'Your account must be active to withdraw.')
        return redirect('wallet:dashboard')
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            if amount > user.balance:
                messages.error(request, 'Insufficient balance.')
            else:
                txn = form.save(commit=False)
                txn.user = user
                txn.type = 'withdraw'
                txn.save()
                messages.success(request, 'Withdrawal request submitted!')
                return redirect('wallet:transactions')
    else:
        form = WithdrawForm()
    return render(request, 'wallet/withdraw.html', {'form': form, 'balance': user.balance})

@login_required
def transactions(request):
    txn_type = request.GET.get('type', '')
    txns = request.user.transactions.all()
    if txn_type:
        txns = txns.filter(type=txn_type)
    return render(request, 'wallet/transactions.html', {'txns': txns, 'filter': txn_type})

@login_required
def get_balance(request):
    return JsonResponse({'balance': str(request.user.balance)})

@login_required
def notifications(request):
    notifs = request.user.notifications.all()
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return render(request, 'wallet/notifications.html', {'notifs': notifs})

@login_required
def products(request):
    prods = Product.objects.filter(is_active=True)
    return render(request, 'wallet/products.html', {'products': prods})

@login_required
def buy_product(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    user = request.user
    if user.account_status != 'active':
        messages.error(request, 'Account must be active to purchase.')
        return redirect('wallet:products')
    if user.balance < product.price:
        messages.error(request, 'Insufficient wallet balance.')
        return redirect('wallet:products')
    user.balance -= product.price
    user.save()
    Order.objects.create(user=user, product=product, quantity=1, total_amount=product.price)
    Notification.objects.create(user=user, message=f'You purchased {product.name} for ₹{product.price}')
    messages.success(request, f'Successfully purchased {product.name}!')
    return redirect('wallet:dashboard')
