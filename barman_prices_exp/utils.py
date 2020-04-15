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

import math


def compute_price(price, constant_margin, variable_margin, form_parameter, scope):
    """Compute price using exponential function
    
    Args:
        price (int): purchase price
        constant_margin (int): constant margin
        variable_margin (int): variable margin
        form_parameter (int): form parameter
        scope (int): scope

    When the price is greater or equal than the scope, only the constant margin is used.
    When the price is lower than the scope, variable margin * exp(-form parameter/(x-scope)**2) is added to the constant margin
    
    Returns:
        int: computed price
    """
    if price < scope:
        return float(price) * (
            1
            + float(constant_margin)
            + float(variable_margin) * math.exp(-form_parameter / (price - scope) ** 2)
        )
    return price * (1 + constant_margin)
