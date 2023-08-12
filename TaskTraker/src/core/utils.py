import logging
from os import getenv
from typing import TypeVar, Callable, Any, Final

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

from core.services.campaign_service import CampaignService
from core.services.batch_service import BatchService
from core.services.stats_service import StatsService
from core.services.push_service import PushService
from core.services.invalid_push_tokens_service import InvalidPushTokenService

from core.db_mysql.repository.campaign_repository import CampaignRepository
from core.db_mysql.repository.push_repository import PushRepository
from core.db_mysql.repository.batch_repository import BatchRepository
from core.db_mysql.repository.user_batch_repository import UserBatchRepository
from core.db_mysql.repository.invalid_push_tokens_repository import InvalidPushTokenRepository
from core.db_clickhouse.repository.stats_repository import StatsRepository
from admin_api.src.core.settings import get_settings


F = TypeVar("F", bound=Callable[..., Any])
APP_ENV: Final = getenv('APP_ENV', 'local')
settings = get_settings()


def init_sentry(fn: F) -> F:
    sentry_logging = LoggingIntegration(
        level=logging.INFO,  # Capture info and above as breadcrumbs
        event_level=logging.ERROR  # Send errors as events
    )
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        integrations=[
            sentry_logging,
        ],
        environment=APP_ENV
    )

    return fn


async def get_campaign_service_callback(sessions):
    async for session in sessions:
        campaign_repository = CampaignRepository(session)
        push_repository = PushRepository(session)
        campaign_service = CampaignService(campaign_repository, push_repository)
        return campaign_service


async def get_batch_campaign_service_callback(sessions):
    async for session in sessions:
        batch_repository = BatchRepository(session)
        campaign_repository = CampaignRepository(session)
        user_batch_repository = UserBatchRepository(session)
        push_repository = PushRepository(session)
        invalid_push_token_repository = InvalidPushTokenRepository(session)
        invalid_push_token_service = InvalidPushTokenService(invalid_push_token_repository)
        batch_service = BatchService(batch_repository, user_batch_repository, campaign_repository)
        campaign_service = CampaignService(campaign_repository, push_repository)
        return batch_service, campaign_service, invalid_push_token_service


async def get_batch_campaign_push_service_callback(sessions):
    async for session in sessions:
        batch_repository = BatchRepository(session)
        campaign_repository = CampaignRepository(session)
        user_batch_repository = UserBatchRepository(session)
        push_repository = PushRepository(session)
        invalid_push_token_repository = InvalidPushTokenRepository(session)
        invalid_push_token_service = InvalidPushTokenService(invalid_push_token_repository)
        batch_service = BatchService(batch_repository, user_batch_repository, campaign_repository)
        campaign_service = CampaignService(campaign_repository, push_repository)
        push_service = PushService(push_repository)
        return batch_service, campaign_service, push_service, invalid_push_token_service


async def get_batch_service_callback(sessions):
    async for session in sessions:
        batch_repository = BatchRepository(session)
        campaign_repository = CampaignRepository(session)
        user_batch_repository = UserBatchRepository(session)
        batch_service = BatchService(batch_repository, user_batch_repository, campaign_repository)
        return batch_service


async def get_stats_service_callback(sessions):
    async for session in sessions:
        stats_repository = StatsRepository(session)
        stats_service = StatsService(stats_repository)
        return stats_service





