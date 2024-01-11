import random

from playwright.sync_api import Page, Browser, BrowserContext
import pytest

from shared.config.staging import staging_config


@pytest.mark.skip()
def test_signup(logged_in_context: tuple[Page, BrowserContext, Browser]):
    page, _, _ = logged_in_context
    num = str(random.randint(1000, 9999))
    page.goto(staging_config.BASE_URL.replace('://', '://signup.') + 'auth/register')
    page.get_by_label('Company name').fill(f'Test Company {num}')
    page.get_by_label('Subdomain').fill(f'test-company-{num}')
    page.get_by_label('Email Address').fill(f'duytd7544+{num}@gmail.com')
    page.get_by_label('Sign up').click()
    page.wait_for_load_state('networkidle')
    side_menu_xpath = '//div[@data-role="site-app-menu"]'
    page.wait_for_selector(side_menu_xpath)


# def test_(logged_in_context: tuple[Page, BrowserContext, Browser]):
#     page, _, _ = logged_in_context
#     page.goto('https://staging.kleversuite.net/settings/role/list')
#     page.wait_for_load_state('domcontentloaded')
#     page.get_by_role('button', name='Create').first.click()
#     page.get_by_placeholder('Type your role name here').fill('Project Create')
#     page.locator('div[role="button"]').get_by_text('Projects').first.click()
#     page.locator('tbody[template-perm-modal]').locator('tr:has-text("Own Tasks")').locator(
#         'td'
#     ).nth(Permission.CREATE.value).click()
#     page.get_by_role('button', name='Save').click()
#     page.wait_for_timeout(1000)

#     page.goto('https://staging.kleversuite.net/settings/group/list')
#     page.wait_for_timeout(1000)
#     page.get_by_role('button', name='Create').first.click()

#     page.goto('https://staging.kleversuite.net/project/')
#     page.wait_for_timeout(10000)
