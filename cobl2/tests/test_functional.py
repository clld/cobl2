import pytest

pytest_plugins = ['clld']


@pytest.mark.parametrize(
    "method,path",
    [
        ('get_html', '/'),
        ('get_dt', '/cognatesets?iSortingCols=1&iSortCol_0=1'),
        ('get_dt', '/cognatesets?sSearch_1=right'),
    ])
def test_pages(app, method, path):
    getattr(app, method)(path)
