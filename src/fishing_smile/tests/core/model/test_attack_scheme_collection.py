from pathlib import Path

import pytest

from fishing_smile.settings import get_settings
from fishing_smile.core.model import *


@pytest.mark.parametrize(
    'scheme_name',
    list(standard_schemes.schemes),
)
def test_get_standard_schemes(scheme_name):
    scheme = standard_schemes.get(scheme_name)
    assert scheme.name == scheme_name


def test_get_scheme_name_not_indexed_in_standard_collection():
    with pytest.raises(ValueError, match = 'not indexed'):
        scheme = standard_schemes.get('scheme_does_not_exist')


@pytest.fixture(name = 'schemes')
def get_test_schemes():
    schemes = AttackSchemeCollection()
    schemes.index_schemes(Path(__file__).parent / 'test_cases/scheme')
    return schemes


def test_scheme_cache(schemes):
    scheme_name = 'scheme_with_external_template_file'
    meta = schemes.get_meta(scheme_name)
    assert meta.cache_mtime is None

    scheme = schemes.get(scheme_name)
    assert meta.cache_mtime != None, 'mtime must be recorded when cache is first populated'
    first = meta.cache

    scheme = schemes.get(scheme_name)
    second = meta.cache
    assert first is second, 'If source mtime did not change, cached object should be exactly the same object as before'

    meta.source.touch()
    scheme = schemes.get(scheme_name)
    after_touching = meta.cache
    if get_settings().deployment_mode == 'development':
        assert second is not after_touching, 'once touched, cache must be reloaded'
        assert second == after_touching, 'content must stays the same as file is only touched but not edited'
    else:
        assert second is after_touching, 'Template auto-reloading is disabled in non-development mode'


def test_get_template_from_jinja_env(schemes):
    template = schemes.jinja_env.get_template('scheme_with_external_template_file/html/html/relative')
    rendered = template.render()
    assert rendered == 'alert(1);'


def test_get_invalid_template_from_jinja_env(schemes):
    expects_invalid_format = pytest.raises(ValueError, match = 'Template name must follow .* format')
    with expects_invalid_format:
        template = schemes.jinja_env.get_template('does not follow naming format')
    with pytest.raises(ValueError):
        template = schemes.jinja_env.get_template('scheme_name_does_not_exist/component_kind/component_name/template_name')
    with expects_invalid_format:
        template = schemes.jinja_env.get_template('empty/component_name_does_not_exist/template_name')
    # NOTE: Is it better to convert to ValueError for uniformity?
    with pytest.raises(KeyError):
        template = schemes.jinja_env.get_template('scheme_with_external_template_file/html/html/template_name_does_not_exist')


def test_string_template_cache(schemes):
    scheme_name = 'scheme_with_external_template_file'
    component_kind = 'html'
    component_name = 'html'
    template_name = 'url'
    jinja_key = f'{scheme_name}/{component_kind}/{component_name}/{template_name}'
    source = schemes.get_meta(scheme_name).source

    first = schemes.jinja_env.get_template(jinja_key)
    second = schemes.jinja_env.get_template(jinja_key)
    assert first is second
    assert second.is_up_to_date

    source.touch()
    assert not second.is_up_to_date
    after_touching = schemes.jinja_env.get_template(jinja_key)
    if get_settings().deployment_mode == 'development':
        assert second is not after_touching
    else:
        assert second is after_touching, 'Template auto-reloading is disabled in non-development mode'


def test_file_template_cache(schemes):
    scheme_name = 'scheme_with_external_template_file'
    component_kind = 'html'
    component_name = 'html'
    template_name = 'relative'
    jinja_key = f'{scheme_name}/{component_kind}/{component_name}/{template_name}'
    source = schemes.get(scheme_name).components.first(name = component_name).templates[template_name]._effective_path

    first = schemes.jinja_env.get_template(jinja_key)
    second = schemes.jinja_env.get_template(jinja_key)
    assert first is second
    assert second.is_up_to_date

    source.touch()
    assert not second.is_up_to_date
    after_touching = schemes.jinja_env.get_template(jinja_key)
    if get_settings().deployment_mode == 'development':
        assert second is not after_touching
    else:
        assert second is after_touching, 'Template auto-reloading is disabled in non-development mode'
