from sphinx.application import Sphinx, Config

__version__ = '0.0.1'


def kotoba_conf(app: Sphinx, config: Config):
    after_load = '''
        (function(f) {
            if (document.readyState != 'loading') {
                f()
            } else if (document.addEventListener) {
                document.addEventListener('DOMContentLoaded', f)
            } else {
                document.attachEvent('onreadystatechange', () => {
                    if (document.readyState == 'complete') f();
                })
            }
        }(%s));
    '''

    conf: dict = config.kotoba

    if conf != None and not isinstance(conf, dict):
        raise ValueError('Configuration for kotoba should be a dictionary')

    dokieli: dict = conf.get('dokieli')
    giscus: dict = conf.get('giscus')
    hypothesis: dict = conf.get('hypothesis')
    utterances: dict = conf.get('utterances')

    extra_config = {'async': 'async'}

    if hypothesis:
        app.add_js_file(
            'https://hypothes.is/embed.js',
            kind='hypothesis', **extra_config
        )

    if dokieli:
        app.add_js_file(
            'https://dokie.li/scripts/dokieli.js',
            kind='dokieli', **extra_config
        )
        app.add_css_file(
            'https://dokie.li/media/css/dokieli.css',
            media='all'
        )

    if utterances:
        available_settings = {'repo', 'issue-term', 'label', 'theme', 'crossorigin'}
        if 'repo' not in utterances:
            raise ValueError('To use utterances, you must provide a repository')

        js = \
        '() => {'\
            'var script = document.createElement("script");'\
            'script.type = "text/javascript";'\
            'script.src = "https://utteranc.es/client.js";'\
            'script.async = "async";'

        for k, v in utterances.items():
            if k not in available_settings:
                raise ValueError(f'Unknown setting for utterances: {k}')
            else:
                js += f'script.setAttribute("{k}", "{v}");'
        js += \
            'sections = document.querySelectorAll("div.section, section");'\
            'if (sections !== null && sections.length > 0) {'\
                'section = sections[sections.length - 1];'\
                'section.appendChild(script);'\
            '}'\
        '}'

        js = after_load % js
        app.add_js_file(None, body=js, kind='utterances')

    if giscus:
        available_settings = {
            'data-repo', 'data-repo-id',
            'data-category', 'data-category-id',
            'data-mapping', 'data-strict',
            'data-reactions-enabled',
            'data-emit-metadata',
            'data-input-position',
            'data-theme', 'data-lang',
            'crossorigin',
        }
        if 'data-repo' not in giscus or 'data-repo-id' not in giscus:
            raise ValueError('To use giscus, you must provide a repository')

        js = \
        '() => {'\
            'var script = document.createElement("script");'\
            'script.type = "text/javascript";'\
            'script.src = "https://giscus.app/client.js";'\
            'script.async = "async";'

        for k, v in giscus.items():
            if k not in available_settings:
                raise ValueError(f'Unknown setting for utterances: {k}')
            else:
                js += f'script.setAttribute("{k}", "{v}");'

        js += \
            'sections = document.querySelectorAll("div.section, section");'\
            'if (sections !== null && sections.length > 0) {'\
                'section = sections[sections.length - 1];'\
                'section.appendChild(script);'\
            '}'\
        '}'

        js = after_load % js
        app.add_js_file(None, body=js, kind='giscus')

def setup(app: Sphinx):
    app.add_config_value("kotoba", None, "html")

    app.connect("config-inited", kotoba_conf)

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
