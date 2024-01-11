from .base import Config, Credentials, Role

staging_config = Config(
    BASE_URL='https://staging.kleversuite.net/',
    CREDENTIALS_BY_ROLE={
        Role.PLATFORM_ADMIN: Credentials(
            EMAIL='super.admin@stagingtokyotechies.com',
            PASSWORD='SupppaaaaUser@12345',
        ),
        Role.ORG_ADMIN: Credentials(
            EMAIL='klever.admin@stagingtokyotechies.com',
            PASSWORD='SZAsdksd78##$123',
        ),
        Role.ORG_USER: Credentials(
            EMAIL='normal@user.com',
            PASSWORD='NormalUser@1234',
        ),
        Role.PUBLIC_USER: Credentials(
            EMAIL='normal@user.com',
            PASSWORD='D^f65P@pTm5M',
        ),
    },
)
