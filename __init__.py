from flask import (
    render_template, 
    Blueprint,
    request
)

from CTFd.utils.decorators import admins_only, get_config
from CTFd.plugins import register_plugin_assets_directory, register_plugin_script, override_template
from CTFd.models import db

import os

assets = Blueprint("assets", __name__, template_folder="assets")


class OpenVPN(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    server_ip = db.Column(db.String(16))
    server_port = db.Column(db.String(4))
    ca_cert = db.Column(db.Text)
    client_cert = db.Column(db.Text)
    ta_key = db.Column(db.Text)

    def __init__(self, server_ip, server_port, ca_cert, client_cert, ta_key):
        self.server_ip = server_ip
        self.server_port = server_port
        self.ca_cert = ca_cert
        self.client_cert = client_cert
        self.ta_key = ta_key
  
def load(app):
    app.db.create_all()
    app.register_blueprint(assets)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    template_path = os.path.join(dir_path, 'templates/settings_new.html')
    override_template('settings.html', open(template_path).read())

    register_plugin_assets_directory(app, base_path='/plugins/ctfd-plugin-openvpn/assets/')
    register_plugin_script('/plugins/ctfd-plugin-openvpn/assets/settings_new.js')

    print("OpenVPN-Cfg plugin is ready!")
    

@assets.route('/admin/openvpn', methods=['GET', 'POST'])
@admins_only
def ovpncfg():
    ovpn = db.session.query(OpenVPN).get(1)
    if request.method == 'GET':
        return render_template('ovpnconfig.html', ovpn=ovpn), db.session.close()
    elif request.method == 'POST':
        server_ip = request.form.get('server_ip')
        server_port = request.form.get('server_port')
        ca_cert = request.form.get('ca_cert')
        client_cert = request.form.get('client_cert')
        ta_key = request.form.get('ta_key')
        if ovpn == None:
            ovpnData = OpenVPN(server_ip=server_ip, server_port=server_port, ca_cert=ca_cert, client_cert=client_cert, ta_key=ta_key)
            db.session.add(ovpnData)
        elif ovpn != None:
            ovpn.server_ip = server_ip
            ovpn.server_port = server_port
            ovpn.ca_cert = ca_cert
            ovpn.client_cert = client_cert
            ovpn.ta_key = ta_key
        db.session.commit()
        ovpn = db.session.query(OpenVPN).get(1)
        return render_template('ovpnconfig.html', ovpn=ovpn), db.session.close()