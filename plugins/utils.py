def settings_on_change(settings, keys, clear=False):
    """Listen settings change. Adopted from Terminus."""

    if not isinstance(keys, list):
        singleton = True
        keys = [keys]
    else:
        singleton = False
    _cached = {}
    for key in keys:
        _cached[key] = settings.get(key, None)

    tag = "handyllm_{}_{}".format(settings.settings_id, ".".join(keys))

    if clear:
        settings.clear_on_change(tag)
        return

    def check_cache_values(on_change):
        run_on_change = False

        for key in keys:
            value = settings.get(key)
            if _cached[key] != value:
                _cached[key] = value
                run_on_change = True

        if run_on_change:
            if singleton and len(_cached) == 1:
                on_change(list(_cached.values())[0])
            else:
                on_change(_cached)

    def _(on_change):
        settings.add_on_change(tag, lambda: check_cache_values(on_change))

    return _
