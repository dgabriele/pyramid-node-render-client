def includeme(config):
    factory = 'pyramid_react.renderer.ReactRenderer'
    template_extension = config.registry.settings['react.extension']
    config.add_renderer(template_extension, factory=factory)
