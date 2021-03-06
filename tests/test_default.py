import testinfra.utils.ansible_runner
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/ansible_inventory').get_hosts('all')


def test_service_running_and_enabled(Service):
    service = Service('nginx')
    assert service.is_running
    assert service.is_enabled


@pytest.mark.parametrize("uri,expecturi,expectcode", [
    ('/map?search=abc1', '/redirectmap?query=def2', 302),
    ('/map?search=other', '/redirectmap', 302),
    ('/direct/', '/redirect', 301),
    ('/redirect/', '/default', 302),
    ('/map', '/redirectmap', 302),
    ('/default', '/default/', 301),
])
def test_redirects(Command, uri, expecturi, expectcode):
    out = Command.check_output("curl -I http://localhost%s" % uri)
    assert ('HTTP/1.1 %d' % expectcode) in out
    assert ('Location: http://localhost%s' % expecturi) in out


def test_get_alias(Command):
    out = Command.check_output("curl http://localhost/default/")
    assert '<title>Welcome to nginx!</title>' in out
