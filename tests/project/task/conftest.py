from urllib.parse import urljoin

from playwright.sync_api import Page, Browser, BrowserContext
import pytest

from config.base import UrlPath
from config.staging import staging_config


@pytest.fixture(scope='session')
def create_project(logged_in_context: tuple[Page, BrowserContext, Browser]):
    page, _, _ = logged_in_context
    page.goto(urljoin(staging_config.BASE_URL, UrlPath.PROJECT.value))
    page.locator('button[data-role="project-add-trigger"]:visible').first.click()
    page.get_by_label('Name').fill('Test Project')
    page.locator('button[data-role="project-form-submit"]').first.click()

    yield logged_in_context


@pytest.fixture(scope='session')
def create_project_1(logged_in_context: tuple[Page, BrowserContext, Browser]):
    page, _, _ = logged_in_context
    page.goto(urljoin(staging_config.BASE_URL, UrlPath.PROJECT.value))
    page.locator('button[data-role="project-add-trigger"]:visible').first.click()
    page.get_by_label('Name').fill('Test Project 1')
    page.locator('button[data-role="project-form-submit"]').first.click()

    yield logged_in_context
