# docutils GLEP support
# Copyright (c) 2022 Michał Górny
# Copyright (c) 2017 Gentoo Foundation
# Placed in public domain
# based on PEP code by:
#
# Author: David Goodger
# Contact: goodger@users.sourceforge.net
# Revision: $Revision: 1.1 $
# Date: $Date: 2004/07/20 18:23:59 $
# Copyright: This module has been placed in the public domain.

"""
Gentoo Linux Enhancement Proposal (GLEP) Reader.
"""

__docformat__ = 'reStructuredText'

from email.message import EmailMessage

import re

import yaml

from docutils import DataError
from docutils.parsers import rst
from docutils.readers import pep as pepsreader
from docutils.transforms import peps
from docutils_glep.transforms import GLEPHeaders


class PreambledRstParser(rst.Parser):
    """GLEP parser class capable of reading YAML preamble."""

    ESCAPE_RE = re.compile(r'([`~!#$%^&*\(\)-+=\[\]\{\};:.\'"<>?/|\\])')

    def parse(self, inputstring, document):
        if inputstring.startswith('---\n'):
            _, yaml_text, glep_text = inputstring.split('---\n', 2)
            assert not _
            try:
                yaml_data = yaml.safe_load(yaml_text)
            except Exception as e:
                raise DataError('Header preamble is not valid YAML:\n%s' % e)
            rfc_header = EmailMessage()
            for k, v in yaml_data.items():
                if v is None:
                    v = ""
                rfc_header[k] = self.ESCAPE_RE.sub(r"\\\1", str(v))
            inputstring = str(rfc_header) + glep_text

        super(PreambledRstParser, self).parse(inputstring, document)


class Reader(pepsreader.Reader):

    """Glep reader class with minor modifications to the pep reader."""

    supported = ('glep',)
    """Contexts this reader supports."""

    def get_transforms(self):
        """Parse headers for gleps, not peps."""
        transforms = pepsreader.Reader.get_transforms(self)
        transforms.remove(peps.Headers)
        transforms.append(GLEPHeaders)
        return transforms

    def __init__(self, parser=None, parser_name=None):
        """`parser` should be ``None``."""
        if parser is None:
            parser = PreambledRstParser(rfc2822=True, inliner=self.inliner_class())
        super(Reader, self).__init__(parser, parser_name)
