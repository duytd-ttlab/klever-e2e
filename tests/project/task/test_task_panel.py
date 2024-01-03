from playwright.sync_api import Page, Browser, BrowserContext, expect
import pytest


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

    toast_message = page.locator('*[data-role="toast-message"]:visible').first
    TASK_ID = toast_message.text_content().split(':')[-1]

    yield project


def test_read_task_in_panel(task: tuple[Page, BrowserContext, Browser]):
    global TASK_ID

    page, _, _ = task
    page.locator('.dndrop-draggable-wrapper').get_by_text(TASK_ID).first.click()

    expect(page.locator('.dndrop-draggable-wrapper').get_by_text(TASK_ID).first).to_be_visible()


def test_delete_task_in_stage(task: tuple[Page, BrowserContext, Browser]):
    global TASK_ID

    page, _, _ = task
    page.locator('.taskpanel-index').locator(
        'span[data-bs-original-title="More Actions"]'
    ).first.click()
    page.locator('.dropdown-item').get_by_text('Delete').click()
    page.locator('button[data-role="modal-button-warning-delete"]').click()

    expect(page.locator('.dndrop-draggable-wrapper').get_by_text(TASK_ID).first).not_to_be_visible()
