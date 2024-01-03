from typing import Generator
import pytest
from urllib.parse import urljoin

from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext

from config.staging import staging_config as config, Role


@pytest.fixture(scope='session')
def context() -> Generator[tuple[Page, BrowserContext, Browser], None, None]:
    p = sync_playwright().start()

    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    context.grant_permissions(['clipboard-read', 'clipboard-write'])
    page = context.new_page()

    yield page, context, browser

    p.stop()


def login(page: Page):
    page.goto(urljoin(config.BASE_URL, 'auth/login'))
    page.get_by_label('Email').fill(config.CREDENTIALS_BY_ROLE[Role.PLATFORM_ADMIN].EMAIL)
    page.get_by_label('Password').fill(config.CREDENTIALS_BY_ROLE[Role.PLATFORM_ADMIN].PASSWORD)
    page.get_by_role('button').get_by_text('Log in').click()
    side_menu_xpath = '//div[@data-role="site-app-menu"]'
    page.wait_for_selector(side_menu_xpath)


@pytest.fixture(scope='session')
def logged_in_context() -> Generator[tuple[Page, BrowserContext, Browser], None, None]:
    p = sync_playwright().start()

    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    context.grant_permissions(['clipboard-read', 'clipboard-write'])
    page = context.new_page()

    login(page)

    yield page, context, browser

    p.stop()
