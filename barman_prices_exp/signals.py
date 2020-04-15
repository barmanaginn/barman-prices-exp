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
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from barman_prices_exp import PluginApp
from barman_prices_exp.models import PriceProfile
from barman_prices_exp.utils import compute_price
from management.models import Keg, Product


@receiver(post_save, sender=Keg)
def update_draft_price(sender, instance, created, **kwargs):
    """Update pint, half pint and quarter pint when a keg is created or changed.
    
    Args:
        sender (model): model of the sender of the signal
        instance (Keg): keg that triggered the signal
        created (bool): true if the keg was juste created
    
    Raises:
        Exception: when no price profile is found for drafts.
    """
    try:
        price_profile = PriceProfile.objects.get(use_for_drafts=True)
    except:
        raise Exception(_("No price profile is defined for drafts."))
    if (created and PluginApp.BarmanPluginMeta.PRICES_EXP_DRAFT_CREATE) or (
        not created and PluginApp.BarmanPluginMeta.PRICES_EXP_DRAFT_UPDATE
    ):
        round = PluginApp.BarmanPluginMeta.PRICES_EXP_ROUND
        base_price = compute_price(
            instance.amount / (2 * instance.capacity),
            price_profile.a,
            price_profile.b,
            price_profile.c,
            price_profile.alpha,
        )
        pint_price = ceil(round * base_price) / round
        instance.pint.amount = pint_price
        instance.pint.save()
        instance.half_pint.amount = ceil(0.5 * round * pint_price) / round
        instance.half_pint.save()
        if instance.quarter_pint:
            instance.quarter_pint.amount = ceil(0.25 * round * pint_price) / round
            instance.quarter_pint.save()


@receiver(post_save, sender=Product)
def update_product_price(sender, instance, created, **kwargs):
    """Update product price when the product is created or changed.
    
    Args:
        sender (model): model of the sender of the signal
        instance (Product): product that triggered the signal
        created (bool): true if the product was juste created
    
    Raises:
        Exception: when no price profile is found for drafts.
    """
    try:
        price_profile = PriceProfile.objects.get(use_for_products=True)
    except:
        raise Exception(_("No price profile is defined for products."))
    if instance.draft_category == Product.DRAFT_NONE:
        if (created and PluginApp.BarmanPluginMeta.PRICES_EXP_PRODUCT_CREATE) or (
            not created and PluginApp.BarmanPluginMeta.PRICES_EXP_PRODUCT_UPDATE
        ):
            round = PluginApp.BarmanPluginMeta.PRICES_EXP_ROUND
            instance.amount = (
                ceil(
                    round
                    * compute_price(
                        instance.amount,
                        price_profile.a,
                        price_profile.b,
                        price_profile.c,
                        price_profile.alpha,
                    )
                )
                / round
            )
            instance.save()
