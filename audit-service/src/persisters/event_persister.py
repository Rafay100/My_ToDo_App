"""
Event Persister for the Audit Service
Persists audit events to storage
"""
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from dapr.aio.clients import DaprClient
from dapr.clients.exceptions import DaprInternalError
import json
import asyncio

logger = logging.getLogger(__name__)


class EventPersister:
    def __init__(self, dapr_client: DaprClient = None):
        self.dapr_client = dapr_client or DaprClient()
        self.state_store_name = "postgresql-statestore"

    async def persist_audit_event(self, audit_data: Dict[str, Any]) -> bool:
        """
        Persist a single audit event to storage
        """
        try:
            # Generate a unique ID for the audit event
            event_id = f"audit_{audit_data.get('entity_id', 'unknown')}_{int(datetime.now().timestamp())}"

            # Prepare the audit event data
            audit_event = {
                'id': event_id,
                'event_type': audit_data.get('event_type', 'unknown'),
                'entity_id': audit_data.get('entity_id'),
                'entity_type': audit_data.get('entity_type', 'system'),
                'user_id': audit_data.get('user_id'),
                'action': audit_data.get('action', 'system_event'),
                'old_values': audit_data.get('old_values', '{}'),
                'new_values': audit_data.get('new_values', '{}'),
                'timestamp': audit_data.get('timestamp', datetime.now().isoformat()),
                'metadata': audit_data.get('metadata', '{}')
            }

            # Save to state store using Dapr
            key = f"audit_event_{event_id}"
            await self.dapr_client.save_state(
                store_name=self.state_store_name,
                key=key,
                value=json.dumps(audit_event)
            )

            logger.info(f"Persisted audit event: {event_id}")
            return True

        except DaprInternalError as e:
            logger.error(f"Dapr error persisting audit event: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Error persisting audit event: {str(e)}")
            return False

    async def persist_bulk_events(self, audit_events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Persist multiple audit events in bulk
        """
        results = {
            'successful': 0,
            'failed': 0,
            'errors': []
        }

        for i, event in enumerate(audit_events):
            try:
                success = await self.persist_audit_event(event)
                if success:
                    results['successful'] += 1
                else:
                    results['failed'] += 1
                    results['errors'].append(f"Failed to persist event {i}")
            except Exception as e:
                results['failed'] += 1
                results['errors'].append(f"Error persisting event {i}: {str(e)}")

        return results

    async def get_audit_events(self, entity_id: Optional[str] = None,
                              entity_type: Optional[str] = None,
                              user_id: Optional[str] = None,
                              limit: int = 100) -> List[Dict[str, Any]]:
        """
        Retrieve audit events based on filters
        """
        try:
            # In a real implementation, this would query the database
            # For now, we'll return an empty list as this is a mock implementation
            logger.info(f"Retrieving audit events with filters - entity_id: {entity_id}, entity_type: {entity_type}, user_id: {user_id}")

            # This would normally query the database with filters
            # Using Dapr state store to retrieve events
            events = []

            # Mock response
            return events

        except Exception as e:
            logger.error(f"Error retrieving audit events: {str(e)}")
            return []

    async def get_audit_events_by_date_range(self, start_date: datetime,
                                           end_date: datetime,
                                           entity_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieve audit events within a date range
        """
        try:
            logger.info(f"Retrieving audit events from {start_date} to {end_date}")

            # This would normally query the database with date range filters
            # Using Dapr state store to retrieve events
            events = []

            # Mock response
            return events

        except Exception as e:
            logger.error(f"Error retrieving audit events by date range: {str(e)}")
            return []

    async def delete_audit_event(self, event_id: str) -> bool:
        """
        Delete a specific audit event (typically not done in audit systems)
        """
        try:
            # In a real audit system, deletion might not be allowed
            # This is just for completeness
            key = f"audit_event_{event_id}"
            await self.dapr_client.delete_state(
                store_name=self.state_store_name,
                key=key
            )

            logger.info(f"Deleted audit event: {event_id}")
            return True

        except Exception as e:
            logger.error(f"Error deleting audit event: {str(e)}")
            return False

    async def health_check(self) -> Dict[str, Any]:
        """
        Check the health of the event persister
        """
        try:
            # Test connection to Dapr state store
            test_key = f"health_test_{int(datetime.now().timestamp())}"
            test_value = json.dumps({'health': 'ok', 'timestamp': datetime.now().isoformat()})

            await self.dapr_client.save_state(
                store_name=self.state_store_name,
                key=test_key,
                value=test_value
            )

            # Retrieve to confirm
            retrieved = await self.dapr_client.get_state(
                store_name=self.state_store_name,
                key=test_key
            )

            # Clean up test entry
            await self.dapr_client.delete_state(
                store_name=self.state_store_name,
                key=test_key
            )

            return {
                'status': 'healthy',
                'store': self.state_store_name,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Audit event persister health check failed: {str(e)}")
            return {
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    async def close(self):
        """Close the event persister and cleanup resources"""
        if self.dapr_client:
            await self.dapr_client.close()