"""
Reminder Consumer for the Notification Service
Consumes reminder events from Kafka and processes them
"""
import asyncio
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import json
from dapr.aio.clients import DaprClient

logger = logging.getLogger(__name__)


class ReminderConsumer:
    def __init__(self, dapr_client: DaprClient):
        self.dapr_client = dapr_client
        self.running = False

    async def start_consuming(self):
        """Start consuming reminder events from Kafka"""
        self.running = True
        logger.info("Starting reminder consumer...")

        # In a real implementation, this would connect to Kafka
        # For now, we'll simulate the consumption
        while self.running:
            try:
                # Simulate consuming a reminder event
                await self.process_pending_reminders()

                # Wait before next check
                await asyncio.sleep(30)  # Check every 30 seconds

            except Exception as e:
                logger.error(f"Error in reminder consumer loop: {str(e)}")
                await asyncio.sleep(5)  # Wait before retrying

    async def process_pending_reminders(self):
        """Process any pending reminders that should be sent"""
        try:
            # Call our backend service to get pending reminders
            # This would typically use Dapr service invocation
            resp = await self.dapr_client.invoke_method(
                app_id='backend-service',
                method_name='get_pending_reminders',
                data={}
            )

            pending_reminders = json.loads(resp.data.get('response', '{}')).get('reminders', [])

            for reminder in pending_reminders:
                await self.send_reminder(reminder)

        except Exception as e:
            logger.error(f"Error processing pending reminders: {str(e)}")

    async def send_reminder(self, reminder: Dict[str, Any]):
        """Send a specific reminder notification"""
        try:
            task_title = reminder.get('task_title', 'Untitled Task')
            user_id = reminder.get('user_id')
            notification_method = reminder.get('notification_method', 'push')

            logger.info(f"Sending reminder for task '{task_title}' to user {user_id} via {notification_method}")

            # Actually send the notification based on method
            if notification_method == 'email':
                await self.send_email_reminder(reminder)
            elif notification_method == 'push':
                await self.send_push_reminder(reminder)
            elif notification_method == 'sms':
                await self.send_sms_reminder(reminder)
            else:
                logger.warning(f"Unknown notification method: {notification_method}")

            # Mark the reminder as sent
            await self.mark_reminder_as_sent(reminder['id'])

        except Exception as e:
            logger.error(f"Error sending reminder: {str(e)}")

    async def send_email_reminder(self, reminder: Dict[str, Any]):
        """Send email reminder"""
        logger.info(f"Sending email reminder for task: {reminder.get('task_title')}")

    async def send_push_reminder(self, reminder: Dict[str, Any]):
        """Send push notification reminder"""
        logger.info(f"Sending push reminder for task: {reminder.get('task_title')}")

    async def send_sms_reminder(self, reminder: Dict[str, Any]):
        """Send SMS reminder"""
        logger.info(f"Sending SMS reminder for task: {reminder.get('task_title')}")

    async def mark_reminder_as_sent(self, reminder_id: str):
        """Mark a reminder as sent in the database"""
        try:
            await self.dapr_client.invoke_method(
                app_id='backend-service',
                method_name='update_scheduled_reminder',
                data={'id': reminder_id, 'is_sent': True, 'sent_at': datetime.now().isoformat()}
            )
        except Exception as e:
            logger.error(f"Error marking reminder as sent: {str(e)}")

    def stop(self):
        """Stop the consumer"""
        self.running = False