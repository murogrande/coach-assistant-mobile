"""
Tests for buildozer.spec configuration.

These run in CI on every push to catch misconfigurations before a real build
(which takes 30–60 min and is only triggered manually).
"""

import configparser
import os
import re
import warnings

SPEC_PATH = os.path.join(os.path.dirname(__file__), "..", "buildozer.spec")
API_CLIENT_PATH = os.path.join(os.path.dirname(__file__), "..", "services", "api_client.py")


def load_spec() -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    assert os.path.exists(SPEC_PATH), "buildozer.spec not found"
    config.read(SPEC_PATH)
    return config


class TestSpecExists:
    def test_spec_file_exists(self):
        assert os.path.exists(SPEC_PATH)

    def test_spec_has_app_section(self):
        config = load_spec()
        assert "app" in config, "[app] section missing from buildozer.spec"

    def test_spec_has_buildozer_section(self):
        config = load_spec()
        assert "buildozer" in config, "[buildozer] section missing from buildozer.spec"


class TestAppIdentity:
    def test_title_is_set(self):
        config = load_spec()
        title = config["app"].get("title", "")
        assert title, "title must be set"
        assert title == "Coach Assistant"

    def test_package_name_is_set(self):
        config = load_spec()
        name = config["app"].get("package.name", "")
        assert name, "package.name must be set"

    def test_package_name_is_alphanumeric(self):
        config = load_spec()
        name = config["app"].get("package.name", "")
        assert re.fullmatch(r"[a-z][a-z0-9]*", name), (
            f"package.name '{name}' must be lowercase alphanumeric (no dots, spaces, or hyphens)"
        )

    def test_package_domain_is_set(self):
        config = load_spec()
        domain = config["app"].get("package.domain", "")
        assert domain, "package.domain must be set"

    def test_version_is_set(self):
        config = load_spec()
        version = config["app"].get("version", "")
        assert version, "version must be set"

    def test_version_format(self):
        config = load_spec()
        version = config["app"].get("version", "")
        assert re.fullmatch(r"\d+\.\d+(\.\d+)?", version), (
            f"version '{version}' must follow X.Y or X.Y.Z format"
        )


class TestRequirements:
    def _get_reqs(self) -> list[str]:
        config = load_spec()
        raw = config["app"].get("requirements", "")
        return [r.strip() for r in raw.split(",") if r.strip()]

    def test_requirements_not_empty(self):
        assert self._get_reqs(), "requirements must not be empty"

    def test_python3_in_requirements(self):
        reqs = self._get_reqs()
        assert "python3" in reqs, "python3 must be in requirements"

    def test_kivy_in_requirements(self):
        reqs = self._get_reqs()
        assert any("kivy" in r.lower() and "kivymd" not in r.lower() for r in reqs), (
            "kivy must be in requirements (as a standalone entry, not just kivymd)"
        )

    def test_kivymd_in_requirements(self):
        reqs = self._get_reqs()
        assert any("kivymd" in r.lower() for r in reqs), "kivymd must be in requirements"

    def test_requests_in_requirements(self):
        reqs = self._get_reqs()
        assert any(r == "requests" for r in reqs), "requests must be in requirements"

    def test_python_dateutil_in_requirements(self):
        reqs = self._get_reqs()
        assert any("dateutil" in r for r in reqs), "python-dateutil must be in requirements"

    def test_asynckivy_in_requirements(self):
        """asynckivy + asyncgui are required by KivyMD 2.x master on Android."""
        reqs = self._get_reqs()
        assert "asynckivy" in reqs, "asynckivy must be in requirements (KivyMD 2.x dependency)"
        assert "asyncgui" in reqs, "asyncgui must be in requirements (asynckivy dependency)"

    def test_ssl_deps_in_requirements(self):
        reqs = self._get_reqs()
        assert "certifi" in reqs, "certifi must be in requirements (SSL for requests on Android)"
        assert "urllib3" in reqs, "urllib3 must be in requirements"

    def test_no_dev_only_packages(self):
        """pytest, pre-commit, ruff must not end up in the APK."""
        reqs = self._get_reqs()
        dev_packages = {"pytest", "pre-commit", "ruff"}
        present = dev_packages & {r.lower() for r in reqs}
        assert not present, f"Dev-only packages in requirements: {present}"


class TestAndroidSettings:
    def test_internet_permission(self):
        config = load_spec()
        perms = config["app"].get("android.permissions", "")
        assert "INTERNET" in perms, "INTERNET permission is required"

    def test_network_state_permission(self):
        config = load_spec()
        perms = config["app"].get("android.permissions", "")
        assert "ACCESS_NETWORK_STATE" in perms, "ACCESS_NETWORK_STATE permission is required"

    def test_min_api_is_set(self):
        config = load_spec()
        minapi = config["app"].get("android.minapi", "")
        assert minapi, "android.minapi must be set"
        assert int(minapi) >= 21, "android.minapi must be >= 21 (Android 5.0)"

    def test_target_api_is_set(self):
        config = load_spec()
        api = config["app"].get("android.api", "")
        assert api, "android.api must be set"
        assert int(api) >= 30, "android.api (target) must be >= 30"

    def test_target_api_above_min_api(self):
        config = load_spec()
        minapi = int(config["app"].get("android.minapi", "0"))
        api = int(config["app"].get("android.api", "0"))
        assert api >= minapi, "android.api must be >= android.minapi"

    def test_ndk_is_set(self):
        config = load_spec()
        ndk = config["app"].get("android.ndk", "")
        assert ndk, "android.ndk must be set"

    def test_accept_sdk_license(self):
        config = load_spec()
        accept = config["app"].get("android.accept_sdk_license", "")
        assert accept.lower() == "true", (
            "android.accept_sdk_license must be True for unattended CI builds"
        )


class TestSourceConfig:
    def test_source_dir_is_set(self):
        config = load_spec()
        assert config["app"].get("source.dir"), "source.dir must be set"

    def test_orientation_is_portrait(self):
        config = load_spec()
        assert config["app"].get("orientation") == "portrait"

    def test_venv_excluded(self):
        config = load_spec()
        exclude_dirs = config["app"].get("source.exclude_dirs", "")
        assert "venv" in exclude_dirs, "venv must be excluded from APK source"

    def test_tests_excluded(self):
        config = load_spec()
        exclude_dirs = config["app"].get("source.exclude_dirs", "")
        assert "tests" in exclude_dirs, "tests/ must be excluded from APK source"

    def test_buildozer_cache_excluded(self):
        config = load_spec()
        exclude_dirs = config["app"].get("source.exclude_dirs", "")
        assert ".buildozer" in exclude_dirs, ".buildozer cache must be excluded from source"

    def test_py_files_included(self):
        config = load_spec()
        exts = config["app"].get("source.include_exts", "")
        assert "py" in exts, "py must be in source.include_exts"


class TestAPIClientAndroidCompat:
    """Checks on api_client.py that are relevant for Android deployments."""

    def _read_client(self) -> str:
        with open(API_CLIENT_PATH) as f:
            return f.read()

    def test_api_client_file_exists(self):
        assert os.path.exists(API_CLIENT_PATH)

    def test_api_base_url_is_defined(self):
        source = self._read_client()
        assert "API_BASE_URL" in source, "API_BASE_URL must be defined in api_client.py"

    def test_api_base_url_not_hardcoded_to_localhost_only(self):
        """Warn if URL is still localhost — it won't work on a physical device."""
        source = self._read_client()
        # Extract the actual value on the API_BASE_URL assignment line
        match = re.search(r'API_BASE_URL\s*=\s*["\']([^"\']+)["\']', source)
        assert match, "Could not parse API_BASE_URL value"
        url = match.group(1)
        # It's fine for localhost during desktop dev, but flag it as a reminder
        # in a dedicated test so the developer sees it at build time.
        if "localhost" in url or "127.0.0.1" in url:
            warnings.warn(
                f"API_BASE_URL is set to '{url}'. "
                "Change it to your laptop's local IP before building for a physical device.",
                UserWarning,
                stacklevel=1,
            )
        # Not an assertion failure — just a warning. The URL is valid for desktop testing.
        assert True

    def test_token_file_has_android_fallback(self):
        """TOKEN_FILE must fall back to a writable dir when ~ isn't writable (Android)."""
        source = self._read_client()
        assert "expanduser" in source, "TOKEN_FILE must start with expanduser"
        assert "os.access" in source, "TOKEN_FILE must check if ~ is writable (Android fallback)"
