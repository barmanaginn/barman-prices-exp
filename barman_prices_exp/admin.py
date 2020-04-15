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

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import PriceProfile


class PriceProfileAdmin(SimpleHistoryAdmin):
    """
    The admin class for :class:`Consumptions <preferences.models.PriceProfile>`.
    """

    list_display = (
        "name",
        "a",
        "b",
        "c",
        "alpha",
        "use_for_drafts",
        "use_for_products",
    )
    ordering = ("name",)
    search_fields = ("name",)
    list_filter = ("use_for_drafts", "use_for_products")


admin.site.register(PriceProfile, PriceProfileAdmin)
