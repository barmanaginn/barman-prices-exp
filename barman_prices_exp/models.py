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

# Define here models or additionnal fields.

from django.db import models
from django.utils.translation import ugettext_lazy as _


class PriceProfile(models.Model):
    """
    Store parameters to compute price.
    """

    class Meta:
        verbose_name = _("price profile")
        verbose_name_plural = _("price profiles")

    name = models.CharField(max_length=255, verbose_name=_("name"))
    a = models.DecimalField(
        verbose_name=_("constant margin"), max_digits=3, decimal_places=2
    )
    b = models.DecimalField(
        verbose_name=_("variable margin"), max_digits=3, decimal_places=2
    )
    c = models.DecimalField(
        verbose_name=_("form parameter"), max_digits=4, decimal_places=2
    )
    alpha = models.DecimalField(verbose_name=_("scope"), max_digits=4, decimal_places=2)
    use_for_drafts = models.BooleanField(
        default=False, verbose_name=_("use for drafts ?")
    )
    use_for_products = models.BooleanField(
        default=False, verbose_name=_("use for products ?")
    )

    def save(self, *args, **kwargs):
        """Override save method to ensure that there is only one price profile
        for drafts and for products.
        """
        if self.use_for_drafts:
            try:
                temp = PriceProfile.objects.get(use_for_drafts=True)
                if self != temp:
                    temp.use_for_drafts = False
                    temp.save()
            except PriceProfile.DoesNotExist:
                pass
        if self.use_for_products:
            try:
                temp = PriceProfile.objects.get(use_for_products=True)
                if self != temp:
                    temp.use_for_products = False
                    temp.save()
            except PriceProfile.DoesNotExist:
                pass
        super(PriceProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
