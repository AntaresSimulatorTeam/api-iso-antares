import json
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from flask import Blueprint, request, jsonify, render_template
from flask_jwt_extended import (  # type: ignore
    create_access_token,
    get_jwt_identity,
    create_refresh_token,
    jwt_required,
)

from antarest.common.auth import Auth
from antarest.common.config import Config
from antarest.login.model import User, Group, Role
from antarest.login.service import LoginService


def create_login_api(service: LoginService, config: Config) -> Blueprint:
    bp = Blueprint(
        "create_login_api",
        __name__,
        template_folder=str(config["_internal.resources_path"] / "templates"),
    )

    auth = Auth(config)

    def generate_tokens(user: User) -> Any:
        access_token = create_access_token(identity=user.to_dict())
        refresh_token = create_refresh_token(identity=user.to_dict())
        return jsonify(
            {
                "user": user.name,
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
        )

    @bp.route("/login", methods=["POST"])
    def login() -> Any:
        username = request.form.get("username") or request.json.get("username")
        password = request.form.get("password") or request.json.get("password")

        if not username:
            return jsonify({"msg": "Missing username parameter"}), 400
        if not password:
            return jsonify({"msg": "Missing password parameter"}), 400

        user = service.authenticate(username, password)
        if not user:
            return jsonify({"msg": "Bad username or password"}), 401

        # Identity can be any data that is json serializable
        resp = generate_tokens(user)

        return (
            resp,
            200,
        )

    @bp.route("/refresh", methods=["POST"])
    @jwt_required(refresh=True)  # type: ignore
    def refresh() -> Any:
        identity = get_jwt_identity()
        user = service.get_user(identity["id"])
        if user:
            resp = generate_tokens(user)

            return (
                resp,
                200,
            )
        else:
            return "Token invalid", 403

    @bp.route("/users", methods=["GET"])
    @auth.protected(roles=[Role.ADMIN])
    def users_get_all(user: User) -> Any:
        return jsonify([u.to_dict() for u in service.get_all_users()])

    @bp.route("/users/<int:id>", methods=["GET"])
    @auth.protected(roles=[Role.ADMIN])
    def users_get_id(id: int, user: User) -> Any:
        u = service.get_user(id)
        if u:
            return jsonify(u.to_dict())
        else:
            return "", 404

    @bp.route("/users", methods=["POST"])
    @auth.protected(roles=[Role.ADMIN])
    def users_create(user: User) -> Any:
        user = User.from_dict(json.loads(request.data))
        return jsonify(service.save_user(user).to_dict())

    @bp.route("/users/<int:id>", methods=["DELETE"])
    @auth.protected(roles=[Role.ADMIN])
    def users_delete(id: int, user: User) -> Any:
        service.delete_user(id)
        return jsonify(id), 200

    @bp.route("/groups", methods=["GET"])
    @auth.protected(roles=[Role.ADMIN])
    def groups_get_all(user: User) -> Any:
        return jsonify([g.to_dict() for g in service.get_all_groups()])

    @bp.route("/groups/<int:id>", methods=["GET"])
    @auth.protected(roles=[Role.ADMIN])
    def groups_get_id(id: int, user: User) -> Any:
        group = service.get_group(id)
        if group:
            return jsonify(group.to_dict())
        else:
            return f"Group {id} not found", 404

    @bp.route("/groups", methods=["POST"])
    @auth.protected(roles=[Role.ADMIN])
    def groups_create(user: User) -> Any:
        group = Group.from_dict(json.loads(request.data))
        return jsonify(service.save_group(group).to_dict())

    @bp.route("/groups/<int:id>", methods=["DELETE"])
    @auth.protected(roles=[Role.ADMIN])
    def groups_delete(id: int, user: User) -> Any:
        service.delete_group(id)
        return jsonify(id), 200

    @bp.route("/protected")
    @auth.protected()
    def protected(user: User) -> Any:
        return f"user id={get_jwt_identity()}"

    return bp
