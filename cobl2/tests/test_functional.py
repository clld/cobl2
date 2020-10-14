import pytest


@pytest.mark.parametrize(
    "method,path",
    [
        ('get_html', '/'),
        ('get_dt', '/cognatesets?iSortingCols=1&iSortCol_0=1'),
        ('get_dt', '/cognatesets?sSearch_1=right'),
        ('get_dt', '/languages?iSortingCols=1&iSortCol_0=1'),
        ('get_html', '/languages/latvian'),
        ('get_html', '/languages/latvian.snippet.html'),
        ('get_html', '/languages.geojson?layer=id'),
        ('get_html', '/languages/hindi.snippet.html?parameter=152'),
        ('get_html', '/clades'),
        ('get_html', '/contributors'),
        ('get_html', '/contributors/1'),
        ('get_html', '/sources'),
        ('get_html', '/sources/345.snippet.html'),
        ('get_html', '/parameters'),
        ('get_html', '/parameters/sit'),
        ('get_html', '/parameters/ant.geojson?layer=ant'),
        ('get_html', '/parameters/back.snippet.html'),
        ('get_html', '/policies'),
        ('get_html', '/cognatesets/5825.geojson?layer=5825'),
        ('get_html', '/cognatesets/5825'),
        ('get_html', '/cognatesets?cladefilter=Baltic'),
        ('get_html', '/cognatesets?cladefilter='),
        ('get_html', '/cognatesets/5007.snippet.html'),
        ('get_html', '/values?sSearch_1=Albanian'),
        ('get_html', '/values/7-208-1'),
    ])
def test_pages(app, method, path):
    getattr(app, method)(path)
