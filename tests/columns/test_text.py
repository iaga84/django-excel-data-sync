# -*- coding: utf-8 -*-
# from __future__ import absolute_import, unicode_literals

import logging

import pytest
from django.db.models import (Field, CharField, URLField, EmailField)
from excel_data_sync.columns import get_column, TextColumn, EmailColumn

logger = logging.getLogger(__name__)


def test_validation():
    f = Field('Field1')
    c = get_column(f)
    v = c._get_validation()
    assert v['validate'] == 'any'


@pytest.mark.parametrize("field", [CharField, URLField])
def test_validator_text_base(field):
    f = field(max_length=40)
    c = get_column(f)
    v = c._get_validation()
    assert isinstance(c, TextColumn)
    assert v['validate'] == 'custom'
    assert v['value'] == '=AND(LEN(THIS)<={})'.format(f.max_length)
    assert v["error_message"] == "String length must be lower than {} chars".format(f.max_length)


@pytest.mark.parametrize("field", [EmailField])
def test_validator_email(field):
    f = field()
    c = get_column(f)
    v = c._get_validation()
    assert isinstance(c, EmailColumn)
    assert v['validate'] == 'custom'
    assert v['value'] == '=AND(SEARCH(".",THIS,(SEARCH("@",THIS,1))+2),LEN(THIS)<=254)'
    assert v["error_message"] == """Not valid email address
String length must be lower than 254 chars"""
