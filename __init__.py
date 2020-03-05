from flask import render_template, Blueprint
from CTFd.utils.decorators import admins_only
from CTFd.plugins import register_plugin_assets_directory

def load(app):
    print("OpenVPN-Cfg plugin is ready!")
    assets = Blueprint("assets", __name__, template_folder="assets")
    app.register_blueprint(assets)
    register_plugin_assets_directory(app, base_path='/plugins/ctfd-plugin-openvpn/assets/')
    @assets.route('/admin/openvpn', methods=['GET'])
    #@admins_only
    def ovpncfg():
        return render_template('config.html') 