from urllib.parse import urljoin

from playwright.sync_api import Page, Browser, BrowserContext, expect

from shared.config.base import UrlPath
from shared.config.staging import staging_config


PROJECT_NAME = 'Test Project'


def test_search_project(logged_in_context: tuple[Page, BrowserContext, Browser]):
    page, _, _ = logged_in_context
    page.goto(urljoin(staging_config.BASE_URL, UrlPath.PROJECT.value))

    expect(
        page.locator('*[data-role="app-header-title-Project"]').first,
        'Should see Project title',
    ).to_have_text('Project')
    expect(
        page.locator('*[data-role="project-card"]').first,
        'Should see at least one project card',
    ).to_have_text


def test_create_project(logged_in_context: tuple[Page, BrowserContext, Browser]):
    global PROJECT_NAME

    page, _, _ = logged_in_context

    page.locator('button[data-role="project-add-trigger"]:visible').first.click()
    page.get_by_label('Name').fill(PROJECT_NAME)
    page.locator('button[data-role="project-form-submit"]').first.click()

    expect(
        page.locator(f'span[data-bs-original-title="{PROJECT_NAME}"]').first,
        'Should see created project title',
    ).to_be_visible()


def test_update_project(logged_in_context: tuple[Page, BrowserContext, Browser]):
    global PROJECT_NAME

    page, _, _ = logged_in_context
    new_project_name = 'New Name'

    page.locator('*[data-role="Settings"]').click()
    page.get_by_label('Name').fill(new_project_name)
    page.get_by_role('button', name='Save').click()

    expect(
        page.locator('*[data-role="toast-message"]:visible').first,
        'Should see success toast message',
    ).to_have_text('Updated Successfully!')
    expect(
        page.get_by_label('Name').first,
        'Should see updated project title',
    ).to_have_value(new_project_name)

    PROJECT_NAME = new_project_name


def test_delete_project(logged_in_context: tuple[Page, BrowserContext, Browser]):
    global PROJECT_NAME

    page, _, _ = logged_in_context

    page.locator('*[data-role="project-archive"]').first.click()
    page.locator('button[data-role="modal-button-warning-archive"]').first.click()
    page.locator('*[data-role="project-move-to-trash"]').click()
    page.locator('button[data-role="modal-button-warning-delete"]').first.click()

    expect(
        page.locator('*[data-role="project-card"]').get_by_text(PROJECT_NAME).first,
    ).to_be_visible()
