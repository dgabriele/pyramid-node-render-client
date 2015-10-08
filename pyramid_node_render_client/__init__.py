def includeme(config):
    factory = 'pyramid_node_render_client.renderer.Renderer'
    template_extension = config.registry.settings['node-render-client.extension']
    config.add_renderer(template_extension, factory=factory)
