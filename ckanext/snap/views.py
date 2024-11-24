"""Views of the snap plugin.

All blueprints added to `__all__` are registered as blueprints inside Flask
app. If you have multiple blueprints, create them inside submodules of
`ckanext.snap.views` and re-export via `__all__`.

Example:
    ```python
    from .custom import custom_bp
    from .data import data_bp

    __all__ = ["custom_bp", "data_bp"]
    ```
"""

from __future__ import annotations

import functools
from typing import Any, cast

from flask import Blueprint
from flask.views import MethodView
from ckan.lib.helpers import Page

import ckan.plugins.toolkit as tk
from ckan import model
from ckan.logic import parse_params

__all__ = ["bp"]

bp = Blueprint("snap", __name__)


# instead of catching exceptions inside every view, it's usually more
# convenient to register handlers for the exception class.
@bp.errorhandler(tk.ObjectNotFound)
def not_found_handler(error: tk.ObjectNotFound) -> tuple[str, int]:
    """Generic handler for ObjectNotFound exception."""
    return (
        tk.render(
            "error_document_template.html",
            {
                "code": 404,
                "content": f"Object not found: {error.message}",
                "name": "Not found",
            },
        ),
        404,
    )


# error handler renders standard error page. If you want to render
# view-specific page with a flash message instead, it's better it try/catch
# inside the view.
@bp.errorhandler(tk.NotAuthorized)
def not_authorized_handler(error: tk.NotAuthorized) -> tuple[str, int]:
    """Generic handler for NotAuthorized exception."""
    return (
        tk.render(
            "error_document_template.html",
            {
                "code": 403,
                "content": error.message or "Not authorized to view this page",
                "name": "Not authorized",
            },
        ),
        403,
    )


def _pager_url(*args: Any, **kwargs: Any) -> str:
    """Generic URL builder for `url` parameter of ckan.lib.pagination.Page.

    It generates pagination link keeping all the parameters from URL and query
    string.
    """
    params = {k: v for k, v in tk.request.args.items() if k != "page"}
    view_args: dict[str, Any] = tk.request.view_args or {}
    params.update(
        dict(view_args.items()),
    )
    params.update(kwargs)
    return tk.h.pager_url(*args, **params)


@bp.route("/dataset/<id>/snapshot")
def package_history(id: str):
    """Basic page."""

    pkg_dict = tk.get_action("package_show")({}, {"id": id})

    rows = 10
    params = tk.request.args
    page = tk.h.get_page_number(params)
    start = rows * page - rows

    result = tk.get_action("snap_snapshot_list")(
        {},
        {
            "target_id": pkg_dict["id"],
            "target_type": "package",
            "start": start,
            "rows": rows,
        },
    )

    pager = Page(
        result["results"],
        items_per_page=rows,
        page=page,
        item_count=result["count"],
        url=functools.partial(_pager_url),
        presliced_list=True,
    )

    return tk.render(
        "snap/package_history.html",
        {"pkg_dict": pkg_dict, "pager": pager},
    )


@bp.route("/dataset/<id>/snapshot/<snapshot_id>/restore", methods=["POST"])
def package_restore(id: str, snapshot_id: str):
    try:
        result = tk.get_action("snap_snapshot_restore")({}, {"id": snapshot_id})

    except tk.ValidationError as err:
        tk.h.flash_error(f"Cannot restore data from snapshot: {err.error_summary}")
        return tk.redirect_to("snap.package_history", id=id)
    except KeyError as err:
        # most likely action does not exist
        tk.h.flash_error(f"Cannot restore data from snapshot: {err}")
        return tk.redirect_to("snap.package_history", id=id)

    return tk.redirect_to("dataset.read", id=result["name"])


@bp.route("/dataset/<id>/snapshot/<snapshot_id>/forget", methods=["POST"])
def package_forget(id: str, snapshot_id: str):
    tk.get_action("snap_snapshot_delete")({}, {"id": snapshot_id})
    return tk.redirect_to("snap.package_history", id=id)
