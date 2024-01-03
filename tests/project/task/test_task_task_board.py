import re

from playwright.sync_api import Page, Browser, BrowserContext, expect

from config.staging import staging_config as config


TASK_ID = None


def create_task(page: Page, task_name: str):
    global TASK_ID

    page.locator('*[data-role="project-stage-kanban-Todo-section-add-task-form"]').first.click()
    page.wait_for_timeout(500)
    page.locator('*[data-role="project-stage-kanban-Todo-add-task-form-task-name"]').first.fill(
        task_name
    )
    page.locator(
        'button[data-role="project-stage-kanban-Todo-add-task-form-add-task-button"]'
    ).first.click()


def test_create_task_in_task_board(project: tuple[Page, BrowserContext, Browser]):
    global TASK_ID

    page, _, _ = project
    create_task(page, 'Test Task')

    toast_message = page.locator('*[data-role="toast-message"]:visible').first
    expect(
        toast_message,
        'Should see success toast message',
    ).to_contain_text('Task link:')
    TASK_ID = toast_message.text_content().split(':')[-1]


# def test_read_task_in_task_board(project: tuple[Page, BrowserContext, Browser]):
#     global TASK_ID

#     page, _, _ = project

#     expect(page.locator('.dndrop-draggable-wrapper').get_by_text(TASK_ID).first).to_be_visible()


# def test_copy_link_task_in_task_board(project: tuple[Page, BrowserContext, Browser]):
#     from .conftest import PROJECT_ID

#     page, _, _ = project
#     page.locator('.overflow-y-auto').filter(has_text=TASK_ID).locator(
#         'span[data-bs-toggle="dropdown"]'
#     ).first.click()
#     page.locator('.dropdown-item').get_by_text('Copy Link').click()

#     expect(page.locator('.dropdown-item').get_by_text('Link copied').first).to_be_visible()
#     # Assert copied link is correct
#     assert (
#         page.evaluate('navigator.clipboard.readText()')
#         == f'{config.BASE_URL}project/{PROJECT_ID}-{TASK_ID}'
#     ), 'Wrong copied link'

#     # Click to dropdown button again to close the dropdown
#     page.locator('.overflow-y-auto').filter(has_text=TASK_ID).locator(
#         'span[data-bs-toggle="dropdown"]'
#     ).first.click()


def test_edit_task_in_task_board(project: tuple[Page, BrowserContext, Browser]):
    global TASK_ID
    page, _, _ = project
    page.locator('.overflow-y-auto').filter(has_text=TASK_ID).locator(
        'span[data-bs-toggle="dropdown"]'
    ).first.click()
    page.locator('.dropdown-item').get_by_text('Edit').click()

    expect(page.locator('button[data-role="project-task-breadcrumb-button"]')).to_have_text(TASK_ID)

    # Click to dropdown button again to close the dropdown
    page.locator('.overflow-y-auto').filter(has_text=TASK_ID).locator(
        'span[data-bs-toggle="dropdown"]'
    ).first.click()


# def test_convert_to_subtask(project: tuple[Page, BrowserContext, Browser]):
#     global TASK_ID
#     page, _, _ = project
#     # create one more task
#     task_1 = 'Test Task 1'
#     create_task(page, task_1)

#     # Open Convert to subtask modal
#     page.locator('.overflow-y-auto').filter(has_text=task_1).locator(
#         'span[data-bs-toggle="dropdown"]'
#     ).first.click()
#     page.locator('.dropdown-item').get_by_text('Convert To Subtask').click()
#     # Convert to subtask
#     page.locator('.dashboard-menu-sub-children').get_by_text('Test Task').first.click()
#     page.get_by_role('button', name='Convert').first.click()
#     # Open task panel
#     page.locator('.dndrop-draggable-wrapper').get_by_text(TASK_ID).first.click()

#     expect(page.locator('.subtask-item-name').get_by_text(task_1)).to_be_visible()

#     # Close task panel
#     page.locator('*[data-bs-dismiss="offcanvas"]').first.click()


def test_archive_task(project: tuple[Page, BrowserContext, Browser]):
    global TASK_ID
    page, _, _ = project
    # create one more task
    task_1 = 'Test Task 1'
    create_task(page, task_1)

    # Open Convert to subtask modal
    page.locator('.overflow-y-auto').filter(has_text=task_1).locator(
        'span[data-bs-toggle="dropdown"]'
    ).first.click()
    page.locator('.dropdown-item').get_by_text('Convert To Subtask').click()
    # Convert to subtask
    page.locator('.dashboard-menu-sub-children').get_by_text('Test Task').first.click()
    page.get_by_role('button', name='Convert').first.click()
    # Open task panel
    page.locator('.dndrop-draggable-wrapper').get_by_text(TASK_ID).first.click()

    expect(page.locator('.subtask-item-name').get_by_text(task_1)).to_be_visible()

    # Close task panel
    page.locator('*[data-bs-dismiss="offcanvas"]').first.click()


def test_delete_task_in_task_board(project: tuple[Page, BrowserContext, Browser]):
    global TASK_ID

    page, _, _ = project
    page.locator('.overflow-y-auto').filter(has_text=TASK_ID).locator(
        'span[data-bs-toggle="dropdown"]'
    ).first.click()
    page.locator('.dropdown-item').get_by_text('Delete').click()
    page.locator('button[data-role="modal-button-warning-delete"]').click()

    expect(page.locator('.dndrop-draggable-wrapper').get_by_text(TASK_ID).first).not_to_be_visible()
