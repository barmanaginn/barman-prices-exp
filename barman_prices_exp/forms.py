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

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import PriceProfile


class PriceProfileForm(forms.ModelForm):
    """
    Form to add and edit a PriceProfile
    """

    class Meta:
        model = PriceProfile
        fields = "__all__"


class ComputePriceForm(forms.Form):
    """
    A form to compute price using price profile.
    """

    price_profile = forms.ModelChoiceField(
        queryset=PriceProfile.objects.all(), label=_("Price profile")
    )
    price = forms.DecimalField(max_digits=10, decimal_places=5, label=_("Price"))
