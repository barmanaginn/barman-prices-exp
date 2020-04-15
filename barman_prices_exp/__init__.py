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

from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from barman.plugin import BarmanPlugin


class PluginApp(BarmanPlugin):
    name = "barman_prices_exp"

    class BarmanPluginMeta:
        name = "Barman prices exp"
        author = "Yoann Pietri"
        description = _("Calculate automatically prices using exponential function")
        version = 0.1
        url = "https://github.com/barmanaginn/barman-prices-exp"
        email = "me@nanoy.fr"

        # Define here urls for navbar. See documentation for more details.
        nav_urls = (
            {
                "text": _("Price profiles"),
                "icon": "fas fa-search-dollar",
                "link": reverse_lazy("plugins:barman_prices_exp:price-profiles-index"),
                "permission": "barman_prices_exp.view_priceprofile",
                "login_required": True,
                "admin_required": False,
                "superuser_required": False,
            },
            {
                "text": _("Compute price"),
                "icon": "fas fa-search-dollar",
                "link": reverse_lazy("plugins:barman_prices_exp:compute-price"),
                "permission": "barman_prices_exp.view_priceprofile",
                "login_required": True,
                "admin_required": False,
                "superuser_required": False,
            },
        )

        # Define here settings specific to this plugin. See documentation for more details.
        settings = (
            {
                "name": "PRICES_EXP_DRAFT_CREATE",
                "description": _(
                    "Auto update prices of pint, half pint and quarter pint at the creation of a keg."
                ),
                "default": True,
            },
            {
                "name": "PRICES_EXP_DRAFT_UPDATE",
                "description": _(
                    "Auto update prices of pint, half pint and quarter pint when a keg is changed."
                ),
                "default": True,
            },
            {
                "name": "PRICES_EXP_PRODUCT_CREATE",
                "description": _(
                    "Replace price by the computed price at the creation of a product."
                ),
                "default": True,
            },
            {
                "name": "PRICES_EXP_PRODUCT_UPDATE",
                "description": _(
                    "Replace price by the computed price awhen a product is changed."
                ),
                "default": False,
            },
            {
                "name": "PRICES_EXP_ROUND",
                "description": _(
                    "Use 10 to round to the tenth and 100 to the hundredth."
                ),
                "default": 10,
            },
        )

        # Define here additionnal info for user profile. See documentation for more details.
        user_profile = ()

    def ready(self):
        from . import signals

        return super().ready()


default_app_config = "barman_prices_exp.PluginApp"
