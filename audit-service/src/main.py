"""
Audit Service for the Advanced Cloud-Native Todo AI Platform
Logs all system events for compliance and debugging
"""
import asyncio
import logging
from datetime import datetime
from typing import Dict, Any
from dapr.aio.clients import DaprClient
from dapr.ext.grpc import App, InvokeMethodRequest
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AuditService:
    def __init__(self):
        self.app = App()
        self.port = 5002

    async def start(self):
        """Start the audit service"""
        logger.info("Starting Audit Service...")

        # Register endpoints
        self.app.add_method_call_handler(
            method='log_audit_event',
            handler=self.handle_log_audit_event
        )

        # Subscribe to all system events to automatically log them
        self.app.add_binding_subscription(
            binding_name='task-updates',
            callback=self.handle_system_event
        )

        # Start the service
        await self.app.run(self.port)

    async def handle_log_audit_event(self, request: InvokeMethodRequest) -> Dict[str, Any]:
        """Handle requests to log an audit event"""
        try:
            # Parse the request data
            request_data = json.loads(request.data.decode('utf-8')) if isinstance(request.data, bytes) else request.data
            logger.info(f"Logging audit event: {request_data}")

            # Persist the audit event
            await self.persist_audit_event(request_data)

            return {'success': True}
        except Exception as e:
            logger.error(f"Error logging audit event: {str(e)}")
            return {'success': False, 'error': str(e)}

    async def handle_system_event(self, request) -> Dict[str, Any]:
        """Handle incoming system events for audit logging"""
        try:
            # Parse the event data
            event_data = json.loads(request.data.decode('utf-8')) if hasattr(request, 'data') else request
            logger.info(f"Auditing system event: {event_data}")

            # Create an audit log entry
            audit_entry = {
                'event_type': event_data.get('event_type', 'unknown'),
                'entity_id': event_data.get('entity_id'),
                'entity_type': event_data.get('entity_type', 'system'),
                'user_id': event_data.get('user_id'),
                'action': event_data.get('action', 'system_event'),
                'old_values': json.dumps(event_data.get('old_values', {})),
                'new_values': json.dumps(event_data.get('new_values', {})),
                'timestamp': datetime.now().isoformat(),
                'metadata': json.dumps(event_data.get('metadata', {}))
            }

            # Persist the audit event
            await self.persist_audit_event(audit_entry)

            return {'success': True}
        except Exception as e:
            logger.error(f"Error auditing system event: {str(e)}")
            return {'success': False, 'error': str(e)}

    async def persist_audit_event(self, audit_data: Dict[str, Any]):
        """Persist the audit event to storage"""
        try:
            # In a real implementation, this would save to a database or log aggregation system
            # For now, we'll just log it
            logger.info(f"AUDIT LOGGED: {audit_data['event_type']} - {audit_data.get('action', 'unknown_action')}")

            # Publish to audit-specific topic if needed
            async with DaprClient() as client:
                await client.publish_event(
                    pubsub_name='kafka-pubsub',
                    topic_name='task-updates',
                    data=json.dumps({
                        'event_type': 'audit_logged',
                        'audit_data': audit_data,
                        'timestamp': datetime.now().isoformat()
                    }),
                    data_content_type='application/json'
                )

        except Exception as e:
            logger.error(f"Error persisting audit event: {str(e)}")

    async def bulk_log_events(self, events: list):
        """Log multiple events in bulk"""
        try:
            results = []
            for event in events:
                result = await self.persist_audit_event(event)
                results.append(result)

            return {'success': True, 'processed_count': len(results)}
        except Exception as e:
            logger.error(f"Error in bulk logging: {str(e)}")
            return {'success': False, 'error': str(e)}

if __name__ == '__main__':
    service = AuditService()
    asyncio.run(service.start())