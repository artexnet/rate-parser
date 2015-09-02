__author__ = 'arthur'

from flask import Blueprint, render_template
from flask.ext.cache import Cache
from config import CACHE_TYPE, CACHE_TIMEOUT


# Blueprint initialization
pages = Blueprint('pages', __name__)

# Cache initialization
cache = Cache(config={'CACHE_TYPE': CACHE_TYPE})


@pages.route('/')
@cache.cached(timeout=CACHE_TIMEOUT)
def index():
    """Default (root) route shows the home page."""
    from managers import banks_manager, rates_manager

    # acquiring number of all banks in DB
    banks_count = banks_manager.get_banks_count()

    # acquiring last update time
    updated = rates_manager.get_last_update_time()
    last_update = None if updated is None else updated.strftime('%Y %d %b, %H:%M')

    # acquiring list of banks with best USD selling rate
    usd_selling_rate = rates_manager.get_usd_selling_min_rate()
    usd_selling_banks = banks_manager.get_usd_selling_best_rate_banks()

    # acquiring list of banks with best EUR selling rate
    eur_selling_rate = rates_manager.get_eur_selling_min_rate()
    eur_selling_banks = banks_manager.get_eur_selling_best_rate_banks()

    # acquiring list of banks with best USD buying rate
    usd_buying_rate = rates_manager.get_usd_buying_max_rate()
    usd_buying_banks = banks_manager.get_usd_buying_best_rate_banks()

    # acquiring list of banks with best EUR buying rate
    eur_buying_rate = rates_manager.get_eur_buying_max_rate()
    eur_buying_banks = banks_manager.get_eur_buying_best_rate_banks()

    # initializing banks data map
    data_map = {
        'usd_selling_rate': usd_selling_rate,
        'eur_selling_rate': eur_selling_rate,
        'usd_buying_rate': usd_buying_rate,
        'eur_buying_rate': eur_buying_rate,
        'usd_selling_banks': usd_selling_banks,
        'eur_selling_banks': eur_selling_banks,
        'usd_buying_banks': usd_buying_banks,
        'eur_buying_banks': eur_buying_banks
    }
    return render_template("index.html", title='Home', banks_count=banks_count, last_updated=last_update, data=data_map)