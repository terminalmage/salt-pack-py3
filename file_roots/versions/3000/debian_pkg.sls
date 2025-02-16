{% import "setup/debian/map.jinja" as buildcfg %}

include:
{% if buildcfg.build_release == 'debian10' %}

    - pkg.salt.3000.debian10

{% elif buildcfg.build_release == 'debian9' %}

    - pkg.python-jinja2.2_9_4.debian9
    - pkg.python-msgpack.0_6_2.debian9
    - pkg.salt.3000.debian9

{% endif %}
