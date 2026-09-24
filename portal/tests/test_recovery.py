"""Offline route regressions. No production credentials or network calls."""
import json
import html
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
TEMP = tempfile.TemporaryDirectory()
os.environ.update(
    CREDENTIALS_PATH=str(Path(TEMP.name) / 'credentials.json'),
    SESSION_SECRET='offline-test-only',
    OIDC_CLIENT_SECRET='offline-test-only',
    KEYCLOAK_ADMIN_PASSWORD='offline-test-only',
)
import main
from fastapi.testclient import TestClient


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(main.app, base_url='https://portal.nigiri-rice.com')

    def login(self, **roles):
        token = main.create_session_token(dict(sub='offline-user', name='Offline Test', roles=[], **roles))
        self.client.cookies.set(main.settings.SESSION_COOKIE_NAME, token)

    def test_every_document_renders_for_authorized_users(self):
        for role in ('is_admin', 'is_developer'):
            self.login(**{role: True})
            for doc_id, doc in main.docs_data.DOCS.items():
                with self.subTest(role=role, document=doc_id):
                    response = self.client.get('/docs/' + doc_id)
                    self.assertEqual(response.status_code, 200)
                    self.assertIn('id="docsNavTree"', response.text)
                    self.assertTrue(doc['title'] in html.unescape(response.text), 'Document title missing')

    def test_anonymous_cannot_read_document(self):
        response = self.client.get('/docs/overview')
        self.assertNotIn('id="docsNavTree"', response.text)

    def test_failed_role_sync_cannot_read_document(self):
        self.login()
        with patch.object(main.jit_sync_service, 'sync_user', new=AsyncMock(return_value={'success': False})):
            response = self.client.get('/docs/overview')
        self.assertNotIn('id="docsNavTree"', response.text)

    def test_missing_document_redirects(self):
        self.login(is_admin=True)
        response = self.client.get('/docs/nonexistent', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.headers['location'].endswith('/docs/overview'))

    def test_static_traversal_blocked(self):
        for prefix in ('/static/', '/portal/static/'):
            for path in ('%2e%2e%2fmain.py', '%2e%2e%5cmain.py', '%2fetc%2fpasswd'):
                with self.subTest(prefix=prefix, path=path):
                    self.assertEqual(self.client.get(prefix + path).status_code, 404)
        self.assertEqual(self.client.get('/static/css/portal.css').status_code, 200)

    def test_new_install_has_no_seed_credentials(self):
        self.assertEqual(json.loads(Path(main.settings.CREDENTIALS_PATH).read_text(encoding="utf-8")), [])

    def test_non_admin_cannot_modify_credentials(self):
        self.login(is_developer=True)
        self.assertEqual(self.client.delete('/api/credentials/nonexistent').status_code, 403)


if __name__ == '__main__':
    unittest.main()
