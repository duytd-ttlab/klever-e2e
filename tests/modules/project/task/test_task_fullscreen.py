import pytest
from playwright.sync_api import Page, Browser, BrowserContext, expect

from shared.config.staging import staging_config as config


TASK_ID = None


@pytest.fixture(scope='module')
def task(project: tuple[Page, BrowserContext, Browser]):
    global TASK_ID

    page, _, _ = project

    page.locator('*[data-role="project-stage-kanban-Todo-section-add-task-form"]').first.click()
    page.wait_for_timeout(500)
    page.locator('*[data-role="project-stage-kanban-Todo-add-task-form-task-name"]').first.fill(
        'Test Task'
    )
    page.locator(
        'button[data-role="project-stage-kanban-Todo-add-task-form-add-task-button"]'
    ).first.click()

    yield project


def test_open_task_fullscreen(task: tuple[Page, BrowserContext, Browser]):
    global TASK_ID

    page, _, _ = task

    page.locator('.overflow-y-auto').filter(has_text=TASK_ID).locator(
        'span[data-bs-toggle="dropdown"]'
    ).first.click()
    page.locator('.dropdown-item').get_by_text('Detail').click()

    # expect(page.locator('button[data-role="project-task-breadcrumb-button"]').first).to_have_text(
    #     TASK_ID
    # )
