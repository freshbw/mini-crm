from glide import (
    AdvancedGlideClientConfiguration,
    BackoffStrategy,
    GlideClient,
    GlideClientConfiguration,
    NodeAddress,
    ServerCredentials,
)

from app.config import Settings


async def create_valkey(settings: Settings) -> GlideClient:
    config = GlideClientConfiguration(
        addresses=[NodeAddress(host=settings.valkey.host, port=settings.valkey.port)],
        request_timeout=1000,
        use_tls=False,
        credentials=ServerCredentials(password=settings.valkey.password.get_secret_value()),
        advanced_config=AdvancedGlideClientConfiguration(connection_timeout=2000),
        reconnect_strategy=BackoffStrategy(
            num_of_retries=5,
            factor=100,
            exponent_base=2,
            jitter_percent=20,
        ),
        lazy_connect=False,
    )
    return await GlideClient.create(config)
