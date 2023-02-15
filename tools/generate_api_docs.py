"""
This script fills the contents of doc/user_guide/API.rst
based on the updated Altair schema.
"""
from os.path import abspath, dirname, join
import sys
import types

# Import Altair from head
ROOT_DIR = abspath(join(dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)
import altair_express as alx  # noqa: E402

API_FILENAME = join(ROOT_DIR, "doc", "user_guide", "API.rst")

API_TEMPLATE = """\
.. _API:
API Reference
=============
This is the class and function reference of Altair Express, and the following content
is generated automatically from the code documentation strings.
Please refer to the `full user guide <http://altair-viz.github.io>`_ for
further details, as this low-level documentation may not be enough to give
full guidelines on their use.
Top-Level Objects
-----------------
.. currentmodule:: altair_express
.. autosummary::
   :toctree: generated/toplevel/
   :nosignatures:
   {toplevel_charts}
Encoding Channels
-----------------
.. currentmodule:: altair_express
.. autosummary::
   :toctree: generated/channels/
   :nosignatures:
   {encoding_wrappers}
API Functions
-------------
.. currentmodule:: altair_express
.. autosummary::
   :toctree: generated/api/
   :nosignatures:
   {api_functions}
Low-Level Schema Wrappers
-------------------------
.. currentmodule:: altair_express
.. autosummary::
   :toctree: generated/core/
   :nosignatures:
   {lowlevel_wrappers}
"""


def iter_objects(
    mod, ignore_private=True, restrict_to_type=None, restrict_to_subclass=None
):
    for name in dir(mod):
        obj = getattr(mod, name)
        if ignore_private:
            if name.startswith("_"):
                continue
        if restrict_to_type is not None:
            if not isinstance(obj, restrict_to_type):
                continue
        if restrict_to_subclass is not None:
            if not (isinstance(obj, type) and issubclass(obj, restrict_to_subclass)):
                continue
        yield name


def toplevel_charts():
    return sorted(iter_objects(alt.api, restrict_to_subclass=alt.TopLevelMixin))


def encoding_wrappers():
    return sorted(iter_objects(alt.channels, restrict_to_subclass=alt.SchemaBase))


def api_functions():
    return sorted(iter_objects(alx.api, restrict_to_type=types.FunctionType))


def lowlevel_wrappers():
    objects = sorted(iter_objects(alt.schema.core, restrict_to_subclass=alt.SchemaBase))
    # The names of these two classes are also used for classes in alt.channels. Due to
    # how imports are set up, these channel classes overwrite the two low-level classes
    # in the top-level Altair namespace. Therefore, they cannot be imported as e.g.
    # altair.Color (which gives you the Channel class) and therefore Sphinx won't
    # be able to produce a documentation page.
    objects = [o for o in objects if o not in ("Color", "Text")]
    return objects