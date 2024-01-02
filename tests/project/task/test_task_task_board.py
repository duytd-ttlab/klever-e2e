import re

import pytest
from playwright.sync_api import Page, Browser, BrowserContext, expect

from config.staging import staging_config as config


TASK_ID = None


def test_create_task_in_task_board(create_project: tuple[Page, BrowserContext, Browser]):
    global TASK_ID

    page, _, _ = create_project
    page.locator('*[data-role="project-stage-kanban-Todo-section-add-task-form"]').first.click()
    page.wait_for_timeout(500)
    page.locator('*[data-role="project-stage-kanban-Todo-add-task-form-task-name"]').first.fill(
        'Test Task'
    )
    page.locator(
        'button[data-role="project-stage-kanban-Todo-add-task-form-add-task-button"]'
    ).first.click()

    toast_message = page.locator('*[data-role="toast-message"]:visible').first
    expect(
        toast_message,
        'Should see success toast message',
    ).to_contain_text('Task link:')
    TASK_ID = toast_message.text_content().split(':')[-1]


def test_read_task_in_task_board(create_project: tuple[Page, BrowserContext, Browser]):
    global TASK_ID

    page, _, _ = create_project

    expect(page.locator('.dndrop-draggable-wrapper').get_by_text(TASK_ID).first).to_be_visible()


def test_copy_link_task_in_task_board(create_project: tuple[Page, BrowserContext, Browser]):
    page, _, _ = create_project
    page.locator('.overflow-y-auto').filter(has_text=TASK_ID).locator(
        'span[data-bs-toggle="dropdown"]'
    ).first.click()
    page.locator('.dropdown-item').get_by_text('Copy Link').click()

    expect(page.locator('.dropdown-item').get_by_text('Link copied').first).to_be_visible()
    # get project id
    current_url = page.evaluate('document.URL')
    matched = re.match(r'.*/project/project/(\d+)/.*', current_url)
    assert matched
    project_id = matched.group(1)
    # Assert copied link is correct
    assert (
        page.evaluate('navigator.clipboard.readText()')
        == f'{config.BASE_URL}project/{project_id}-{TASK_ID}'
    ), 'Wrong copied link'

    # Click to dropdown button again to close the dropdown
    page.locator('.overflow-y-auto').filter(has_text=TASK_ID).locator(
        'span[data-bs-toggle="dropdown"]'
    ).first.click()


def test_edit_task_in_task_board(create_project: tuple[Page, BrowserContext, Browser]):
    global TASK_ID
    page, _, _ = create_project
    page.locator('.overflow-y-auto').filter(has_text=TASK_ID).locator(
        'span[data-bs-toggle="dropdown"]'
    ).first.click()
    page.locator('.dropdown-item').get_by_text('Edit').click()

    expect(page.locator('button[data-role="project-task-breadcrumb-button"]')).to_have_text(TASK_ID)

    # Click to dropdown button again to close the dropdown
    page.locator('.overflow-y-auto').filter(has_text=TASK_ID).locator(
        'span[data-bs-toggle="dropdown"]'
    ).first.click()


def test_delete_task_in_task_board(create_project: tuple[Page, BrowserContext, Browser]):
    global TASK_ID

    page, _, _ = create_project
    page.locator('.overflow-y-auto').filter(has_text=TASK_ID).locator(
        'span[data-bs-toggle="dropdown"]'
    ).first.click()
    page.locator('.dropdown-item').get_by_text('Delete').click()
    page.locator('button[data-role="modal-button-warning-delete"]').click()

    expect(page.locator('.dndrop-draggable-wrapper').get_by_text(TASK_ID).first).not_to_be_visible()
