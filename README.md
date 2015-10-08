pyramid-node-render-client
=====================


Overview
---------------------
This extension blesses your Pyramid app with a renderer that outsources HTML rendering to a Node.js service called [pyramid-node-render-service](https://github.com/dgabriele/pyramid-node-render-service). Pyramid-node-render-service uses [Jade](http://jade-lang.com) templates and is endowed with the ability to “prerender” [React](https://github.com/facebook/react) components.


Configuration
---------------------
In the Paste deploy INI files for your Pyramid app, you have the following configuration options:

 - `node-render-client.extension`: template extension to use in view configuration. For example, `.jade`.

 - `node-render-client.socket`: HTTP or domain socket on which the node service is listening. For example, `localhost:8080` or `/tmp/node-render.sock`.
