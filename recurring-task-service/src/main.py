"""
Recurring Task Service for the Advanced Cloud-Native Todo AI Platform
Generates recurring task instances based on templates
"""
import asyncio
import logging
from datetime import datetime
from typing import Dict, Any
from dapr.aio.clients import DaprClient
from dapr.ext.grpc import App, InvokeMethodRequest
import json
from task_generator import TaskGenerator
from cron_scheduler import CronScheduler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RecurringTaskService:
    def __init__(self):
        self.app = App()
        self.port = 5001
        self.task_generator = TaskGenerator()
        self.cron_scheduler = CronScheduler()

    async def start(self):
        """Start the recurring task service"""
        logger.info("Starting Recurring Task Service...")

        # Initialize the scheduler
        await self.cron_scheduler.initialize()

        # Register endpoints
        self.app.add_method_call_handler(
            method='generate_recurring_tasks',
            handler=self.handle_generate_recurring_tasks
        )

        # Start the service
        await self.app.run(self.port)

    async def handle_generate_recurring_tasks(self, request: InvokeMethodRequest) -> Dict[str, Any]:
        """Handle requests to generate recurring tasks"""
        try:
            # Parse the request data
            request_data = json.loads(request.data.decode('utf-8')) if isinstance(request.data, bytes) else request.data
            logger.info(f"Generating recurring tasks: {request_data}")

            # Generate the recurring tasks
            generated_tasks = await self.task_generator.generate_tasks(request_data)

            # Process the generated tasks
            for task in generated_tasks:
                await self.publish_task_event(task)

            return {
                'success': True,
                'generated_tasks_count': len(generated_tasks),
                'generated_tasks': generated_tasks
            }
        except Exception as e:
            logger.error(f"Error generating recurring tasks: {str(e)}")
            return {'success': False, 'error': str(e)}

    async def publish_task_event(self, task: Dict[str, Any]):
        """Publish a task event to Kafka via Dapr"""
        try:
            async with DaprClient() as client:
                # Publish to task-events topic
                await client.publish_event(
                    pubsub_name='kafka-pubsub',
                    topic_name='task-events',
                    data=json.dumps({
                        'event_type': 'created',
                        'task_data': task,
                        'timestamp': datetime.now().isoformat()
                    }),
                    data_content_type='application/json'
                )
                logger.info(f"Published task event for task: {task.get('title', 'Unknown')}")
        except Exception as e:
            logger.error(f"Error publishing task event: {str(e)}")

if __name__ == '__main__':
    service = RecurringTaskService()
    asyncio.run(service.start())