def parse_db_url(url):
    import re

    if not url:
        return {}

    pattern = r'(?P<protocol>\w+)://(?P<user>\w+):(?P<password>[\w\d]+)@(?P<host>\S+):(?P<port>[\d]+)/(?P<name>[\w\d]+)'
    m = re.match(pattern, url)

    if m is None:
        return {}

    return m.groupdict()
