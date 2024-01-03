import re
from urllib.parse import urljoin

from playwright.sync_api import Page, Browser, BrowserContext
import pytest

from config.base import UrlPath
from config.staging import staging_config as config

PROJECT_NAME = 'Test Project'
PROJECT_ID = None
PROJECT_1_NAME = 'Test Project 1'
PROJECT_1_ID = None


def create_project(page: Page, project_name: str):
    page.goto(urljoin(config.BASE_URL, UrlPath.PROJECT.value))
    page.locator('button[data-role="project-add-trigger"]:visible').first.click()
    page.get_by_label('Name').fill(project_name)
    page.locator('button[data-role="project-form-submit"]').first.click()
    page.wait_for_timeout(500)

    # get project id
    current_url = page.evaluate('document.URL')
    matched = re.match(r'.*/project/project/(\d+)/.*', current_url)
    assert matched
    return matched.group(1)


def delete_project(page: Page, project_id: int):
    page.goto(urljoin(config.BASE_URL, f'/project/project/{project_id}/settings/general'))
    page.locator('*[data-role="project-archive"]').first.click()
    page.locator('button[data-role="modal-button-warning-archive"]').first.click()
    page.locator('*[data-role="project-move-to-trash"]').click()
    page.locator('button[data-role="modal-button-warning-delete"]').first.click()


@pytest.fixture(scope='module')
def project(logged_in_context: tuple[Page, BrowserContext, Browser]):
    global PROJECT_NAME, PROJECT_ID
    page, _, _ = logged_in_context

    PROJECT_ID = create_project(page, PROJECT_NAME)

    yield logged_in_context

    # Delete project
    delete_project(page, PROJECT_ID)


@pytest.fixture(scope='module')
def project_1(logged_in_context: tuple[Page, BrowserContext, Browser]):
    global PROJECT_1_NAME, PROJECT_1_ID
    page, _, _ = logged_in_context

    PROJECT_1_ID = create_project(page, PROJECT_1_NAME)

    yield logged_in_context

    # Delete project
    delete_project(page, PROJECT_1_ID)
