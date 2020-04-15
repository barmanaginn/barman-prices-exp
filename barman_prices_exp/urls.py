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

from django.urls import path

from . import views

app_name = "barman_prices_exp"
urlpatterns = [
    path("price-profiles", views.price_profiles_index, name="price-profiles-index"),
    path("price-profiles/new", views.add_price_profile, name="price-profiles-add"),
    path(
        "price-profiles/<int:pk>/edit",
        views.edit_price_profile,
        name="price-profiles-edit",
    ),
    path(
        "price-profiles/<int:pk>/delete",
        views.delete_price_profile,
        name="price-profiles-delete",
    ),
    path("compute-price", views.compute_price_view, name="compute-price"),
]
