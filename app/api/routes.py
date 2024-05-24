from flask import Blueprint, jsonify, request, render_template
from models import Server, server_schema, server_schema_list, db, User
from helpers import token_required

api = Blueprint("api", __name__, url_prefix="/api")

@api.route("/servers", methods = ["POST"])
@token_required
def add_server(current_user_token):
    ip = request.json["ip"]
    port = request.json["port"]
    hostname = request.json["hostname"]
    version = request.json["version"]
    motd = request.json["motd"]
    max_players = request.json["max_players"]
    user_token = current_user_token.token

    print(f"BIG TESTER: {current_user_token}")

    server = Server(ip, port, hostname, version, motd, max_players, user_token=user_token)

    db.session.add(server)
    db.session.commit()

    response = server_schema.dump(server)
    return jsonify(response)

@api.route("/servers", methods = ["GET"])
@token_required
def show_all_servers(current_user_token):
    owner = current_user_token.token
    servers = Server.query.filter_by(user_token = owner).all()
    response = server_schema_list.dump(servers)
    return jsonify(response)

@api.route("/servers/<id>", methods = ["GET"])
@token_required
def show_server(current_user_token, id):
    server = Server.query.get(id)
    response = server_schema.dump(server)
    return jsonify(response)

@api.route("/servers/<id>", methods = ["POST", "PUT"])
@token_required
def update_server(current_user_token, id):
    server = Server.query.get(id)
    server.ip = request.json["ip"]
    server.port = request.json["port"]
    server.hostname = request.json["hostname"]
    server.version = request.json["version"]
    server.motd = request.json["motd"]
    server.max_players = request.json["max_players"]
    server.user_token = current_user_token.token
    
    db.session.commit()
    response = server_schema.dump(server)
    return jsonify(response)

@api.route("/servers/<id>", methods = ["DELETE"])
@token_required
def delete_server(current_user_token, id):
    server = Server.query.get(id)
    db.session.delete(server)
    db.session.commit()
    response = server_schema.dump(server)
    return jsonify(response)