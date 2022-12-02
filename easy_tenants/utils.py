import threading
from contextlib import contextmanager

from easy_tenants.exceptions import TenantError

state_local = threading.local()


def get_state():
    state_default = {
        "enabled": True,
        "tenant": None,
        "is_admin": False
    }
    state = getattr(state_local, "state", state_default)
    return state


def get_current_tenant():
    state = get_state()

    if state["enabled"] and state["tenant"] is None:
        raise TenantError("Tenant is required in context.")

    return state["tenant"]

def is_admin():
    state = get_state()
    return state["is_admin"]


@contextmanager
def tenant_context(tenant=None, enabled=True, is_admin=False):
    previous_state = get_state()

    new_state = previous_state.copy()
    new_state["enabled"] = enabled
    new_state["tenant"] = tenant
    new_state["is_admin"] = is_admin

    state_local.state = new_state

    try:
        yield
    finally:
        state_local.state = previous_state


@contextmanager
def tenant_context_disabled(is_admin = False):
    with tenant_context(enabled=False, is_admin=is_admin):
        yield
