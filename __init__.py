from flask import (
    render_template, 
    Blueprint,
    request,
    jsonify
)

from CTFd.utils.decorators import admins_only, get_config
from CTFd.plugins import register_plugin_assets_directory
from CTFd.models import db

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
    print("OpenVPN-Cfg plugin is ready!")
    

@assets.route('/admin/openvpn', methods=['GET', 'POST'])
@admins_only
def ovpncfg():
    if request.method == 'GET':
        ovpn = db.session.query(OpenVPN).get(1)
        return render_template('config.html', ovpn=ovpn)
    elif request.method == 'POST':
        server_ip = request.form.get('server_ip')
        server_port = request.form.get('server_port')
        ca_cert = request.form.get('ca_cert')
        client_cert = request.form.get('client_cert')
        ta_key = request.form.get('ta_key')

        ovpn = db.session.query(OpenVPN).get(1)
    
        if ovpn == None:
            ovpnData = OpenVPN(server_ip=server_ip, server_port=server_port, ca_cert=ca_cert, client_cert=client_cert, ta_key=ta_key)
            db.session.add(ovpnData)
            #return render_template('config.html', ovpn=ovpn)
        elif ovpn != None:
            ovpn.server_ip = server_ip
            ovpn.server_port = server_port
            ovpn.ca_cert = ca_cert
            ovpn.client_cert = client_cert
            ovpn.ta_key = ta_key

            
            
    db.session.commit()
    db.session.close()
    return render_template('config.html', ovpn=ovpn)