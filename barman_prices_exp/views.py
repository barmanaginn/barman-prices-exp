# barman-prices-exp - plugin for barman
# Copyright © 2020 Yoann Pietri <me@nanoy.fr>
#
# barman-prices-exp is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# barman-prices-exp is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with barman-prices-exp.  If not, see <https://www.gnu.org/licenses/>.

from math import ceil

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from barman.acl import active_required
from .forms import PriceProfileForm, ComputePriceForm
from .models import PriceProfile
from .utils import compute_price


@active_required
@login_required
@permission_required("preferences.view_priceprofile")
def price_profiles_index(request):
    """Index of the price profiles
    
    Args:
        request (dict): django request object
    
    Returns:
        HttpResponse: django response
    """
    price_profiles = PriceProfile.objects.all()
    return render(
        request,
        "barman_prices_exp/price_profiles_index.html",
        {"price_profiles": price_profiles},
    )


@active_required
@login_required
@permission_required("preferences.add_priceprofile")
def add_price_profile(request):
    """Form to add a price profile
    
    Args:
        request (dict): django request object
    
    Returns:
        HttpResponse: django response
    """
    form = PriceProfileForm(request.POST or None)
    if form.is_valid():
        price_profile = form.save()
        messages.success(
            request,
            _("Price profile {name} was created.").format(name=price_profile.name),
        )
        return redirect(reverse("plugins:barman_prices_exp:price-profiles-index"))
    return render(
        request,
        "form.html",
        {
            "form": form,
            "form_title": _("Add price profile"),
            "form_button": _("Add"),
            "form_button_icon": "fas fa-plus-square",
        },
    )


@active_required
@login_required
@permission_required("preferences.change_priceprofile")
def edit_price_profile(request, pk):
    """Form to edit a price profile
    
    Args:
        request (dict): django request object
        pk (int): primary key of the price profile
    
    Returns:
        HttpResponse: django response
    """
    price_profile = get_object_or_404(PriceProfile, pk=pk)
    form = PriceProfileForm(request.POST or None, instance=price_profile)
    if form.is_valid():
        price_profile = form.save()
        messages.success(
            request,
            _("Price profile {name} was changed.").format(name=price_profile.name),
        )
        return redirect(reverse("plugins:barman_prices_exp:price-profiles-index"))
    return render(
        request,
        "form.html",
        {
            "form": form,
            "form_title": _("Change price profile"),
            "form_button": _("Change"),
            "form_button_icon": "fas fa-pencil-alt",
        },
    )


@active_required
@login_required
@permission_required("preferences.delete_priceprofile")
def delete_price_profile(request, pk):
    """Delete a price profile
    
    Args:
        request (dict): django request object
        pk (int): primary key of the price profile
    
    Returns:
        HttpResponse: redirection to index of price profiles
    """
    price_profile = get_object_or_404(PriceProfile, pk=pk)
    message = _("Price profile {name} was deleted").format(name=price_profile.name)
    price_profile.delete()
    messages.success(request, message)
    return redirect(reverse("plugins:barman_prices_exp:price-profiles-index"))


@active_required
@login_required
def compute_price_view(request):
    """Form to compute prince
    
    Args:
        request (dict): django request object
    
    Returns:
        HttpResponse: django response
    """
    template = _(
        "The price is {price_100} {currency} (rounded to the hundredth) or {price_10} {currency} (rounded to the tenth)."
    )
    form = ComputePriceForm(request.POST or None)
    if form.is_valid():
        price_profile = form.cleaned_data["price_profile"]
        price = compute_price(
            form.cleaned_data["price"],
            price_profile.a,
            price_profile.b,
            price_profile.c,
            price_profile.alpha,
        )
        form_p = template.format(
            currency="€",
            price_100=str(ceil(100 * price) / 100),
            price_10=str(ceil(10 * price) / 10),
        )
    else:
        form_p = ""
    return render(
        request,
        "form.html",
        {
            "form": form,
            "form_title": _("Compute price"),
            "form_button": _("Compute"),
            "form_button_icon": "fas fa-search-dollar",
            "form_p": form_p,
        },
    )
